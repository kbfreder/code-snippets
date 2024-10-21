
import os
import multiprocessing as mp
import logging
from logging.handlers import QueueHandler

from mp_logger import logger_process
from mp_worker import worker_process_func
from mp_config import LOGGER_NAME


# using a Pool must be protected inside this
if __name__ == "__main__":

    # load your raw data
    list_of_data_to_process = [] 

    # must use Queue inside Manager
    with mp.Manager() as manager:

        # create queue, logger that uses queue
        log_queue = manager.Queue()
        logger = logging.getLogger(LOGGER_NAME)
        logger.addHandler(QueueHandler(log_queue))
        logger.setLevel(1) # set level low so all messages captured in queue

        log_dir = os.path.abspath("./logs")
        log_filename = "test.log"
        log_path = os.path.join(log_dir, log_filename)

        num_proc = mp.cpu_count()

        # using a Pool handles a lot of things for you
        with mp.Pool(processes=num_proc) as pool:
            # issue a long running task to receive logging messages
            lp = pool.apply_async(logger_process, 
                args=(log_queue, LOGGER_NAME, log_path))
            logger.info("Test message from main script")

            # do the actual work
            ## NOTE: args to worker_process func get serialized, so keeping them as small 
            ## as possible is beneficial
            results = pool.starmap(
                worker_process_func, 
                [(item, log_queue) for item in list_of_data_to_process]
            )

            # NOTE: must keep everything inside pool to capture all log messages
            logger.info("Done processing!")

            # save results, if desired
            print(results)

            # maybe one final message goes here

            # NOTE: Don't close logger process until you're done logging
            ## this tells logger process to stop
            log_queue.put_nowait(None)
            ## this flushes queue so you get the final messages
            lp.get()
