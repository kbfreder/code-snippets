
import logging
from logging.handlers import QueueHandler
# only needed to demonstrate which worker is involved
import multiprocessing as mp

# just to mock up some "work"
from time import sleep
from random import random

from mp_config import LOGGER_NAME



def worker_process_func(input, queue):

    # get logger & add queue handler
    logger = logging.getLogger(LOGGER_NAME)
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)

    # operte on the input
    process_name = mp.current_process().name
    for i in range(5):
        logger.debug(f"Worker message from {process_name}, step {i}")
        sleep(random())
    
    output = input * input

    # return the output
    return output
