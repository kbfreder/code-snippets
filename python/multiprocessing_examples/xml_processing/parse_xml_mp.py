"""
Parse XML file using python multiprocessing.
"""
import os
import sys
import argparse
from datetime import datetime, timedelta
import math
import multiprocessing as mp
import xml.etree.ElementTree as ET
import pandas as pd
import pickle
import logging
from logging.handlers import QueueHandler

from src.config import (
    DATA_DIR, 
    FILENAME_DICT, 
    LOGGER_NAME
)
from src.xml_parse_utils import (
    construct_ticket_tree_extra_nested_with_dfs,
    extract_text_from_ticket_mp,
)

# from src.basic_utils import logger_process 

def logger_process(queue, logger_name, log_file_path):
    stdout_msg_fmt = '%(asctime)s - %(message)s'
    file_msg_fmt = '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'

    date_fmt = '%Y-%m-%d %H:%M'

    stdout_fmtr = {'fmt': stdout_msg_fmt, 'datefmt': date_fmt}
    file_fmtr = {'fmt': file_msg_fmt, 'datefmt': date_fmt}

    # get the logger
    logger = logging.getLogger(logger_name)
    
    # configure a stream handler
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.INFO)
    s_handler.setFormatter(logging.Formatter(**stdout_fmtr))
    logger.addHandler(s_handler)

    # configure file handler
    f_handler = logging.FileHandler(log_file_path)
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(logging.Formatter(**file_fmtr))
    logger.addHandler(f_handler)

    logger.info('Logger process running.')

    # run logging
    while True:
        message = queue.get()
        if message is None:
            logger.info('Logger process shutting down.')
            break
        logger.handle(message)


def parse_args():
    parser = argparse.ArgumentParser(description="Parse XML from file and extract text")
    parser.add_argument(
        "-f", "--filename_ind",
        help="Filename indicator",
        choices=list(FILENAME_DICT.keys()),
        required=True
    )
    parser.add_argument(
        "-n", "--number",
        help="Number of entries to process. If not specified, all entries will be processed",
    )
    parser.add_argument(
        "--start",
        help="Ticket index to start from",
        type=int
    )
    parser.add_argument(
        "--tickets",
        help="List of ticket indices to process. If not specified, `--number` will be used.",
        nargs='+',
        default=[]
    )
    parser.add_argument(
        "--check",
        help="Print number of tickets & exits",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--skip",
        help="List of ticket indices to skip in process.",
        nargs='+',
        default=[]
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    filename_ind = args.filename_ind
    num_records = args.number
    start_idx = args.start
    ticket_idxs = args.tickets
    skip_idxs = args.skip

    filename = FILENAME_DICT[filename_ind]
    
    filename_stub = os.path.splitext(filename)[0]
    
    if (num_records is not None) & (len(ticket_idxs) > 0):
        print("!! You cannot specify both `--number` and `--tickets` !!")
        print("Please try again.") 
        sys.exit(1)

    if (start_idx is not None) & (len(ticket_idxs) > 0):
        print("!! You cannot specify both `--start` and `--tickets` !!")
        print("Please try again.") 
        sys.exit(1)


    # parse XML records -> get nested tags
    nested_tags_file_name = f'{filename_stub}_nested_tags.pkl'
    nested_tags_file_path = os.path.join(DATA_DIR, 'processed_data', nested_tags_file_name)
    if not os.path.exists(nested_tags_file_path):
        start_time = datetime.now()
        print(f"Starting data preprocessing at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        tree = ET.parse(os.path.join(DATA_DIR, filename))
        root = tree.getroot()
        tags = [child.tag for child in root]
        ticket_data_nested = construct_ticket_tree_extra_nested_with_dfs(tags, root)
        with open (nested_tags_file_path, 'wb') as pf:
            pickle.dump(ticket_data_nested, pf)
        end_time = datetime.now()
        elapsed = (end_time - start_time)/timedelta(minutes=1)
        print(f"Finished data preprocessing in {elapsed:.1f} minutes")
    else:
        print("Opening nested tag file")
        with open (nested_tags_file_path, 'rb') as pf:
            ticket_data_nested = pickle.load(pf)

    total_n = len(ticket_data_nested)

    if args.check:
        print(f"'{filename}' contains {total_n} total tickets")
        sys.exit(0)

    print("Prepping other things")
    if total_n < 1000:
        width = 3
    elif total_n < 10_000:
        width = 4
    else:
        width = 5


    # prep for extracting text
    tix_to_process = ticket_data_nested[:]

    if start_idx is not None:
        tix_to_process = tix_to_process[start_idx:]
    else:
        start_idx = 0

    if num_records is not None:
        num_records = int(num_records)
        num_records_msg = num_records
        tix_to_process = tix_to_process[:num_records]
        end_idx = start_idx + num_records - 1
        save_name = f"tickets-{start_idx:0{width}}-to-{end_idx+1:0{width}}"
    else:
        if len(ticket_idxs) > 0:
            tix_to_process = [ticket_data_nested[int(x)] for x in ticket_idxs]
            num_records_msg = len(ticket_idxs)
            save_name = "specific-tickets"
        else:
            if start_idx == 0:
                num_records_msg = f"all {len(tix_to_process)}"
                save_name = "tickets-all"
            else:
                num_records_msg = len(tix_to_process)
                save_name = f"tickets-{start_idx:0{width}}-to-end"
            end_idx = len(tix_to_process) - 1

    if len(skip_idxs) > 0:
        skip_idxs = [int(x) for x in skip_idxs]
        print(skip_idxs)
        idxs_to_process = range(start_idx, end_idx+1)
        idxs_to_process = [x for x in idxs_to_process if x not in skip_idxs]
        tix_to_process = [ticket_data_nested[int(x)] for x in idxs_to_process]
        num_records_msg = len(tix_to_process)


    # EXTRACT TEXT
    start_time = datetime.now()

    with mp.Manager() as manager:
        print("Setting up logger")
        # create queue, logger that uses queue
        log_queue = manager.Queue()
        logger = logging.getLogger(LOGGER_NAME)
        logger.addHandler(QueueHandler(log_queue))
        logger.setLevel(1) # set level low so all messages captured in queue

        log_dir = os.path.abspath("./logs")
        log_filename = f"{filename_ind}_{save_name}.log"
        log_path = os.path.join(log_dir, log_filename)

        num_proc = mp.cpu_count()

        print("Starting pool")
        with mp.Pool(processes=num_proc) as pool:
            # issue a long running task to receive logging messages
            lp = pool.apply_async(logger_process, 
                args=(log_queue, LOGGER_NAME, log_path))
            print("---------------------------")
            logger.info(f"Processing {filename} - {num_records_msg} records")
            logger.debug(args)

            # do the actual work
            results = pool.starmap(
                extract_text_from_ticket_mp, 
                [(p_dict, log_queue) for p_dict in tix_to_process]
            )
            
            # NOTE: must keep everything inside pool to capture all log messages
            logger.info("Done processing!")

            flat_results = [i for r in results for i in r]
            text_df = pd.DataFrame(flat_results)
                

            out_dir = os.path.join(DATA_DIR, "text_data", filename_ind)
            logger.info(f"Saving restuls to: {out_dir}")
            os.makedirs(out_dir, exist_ok=True)
            text_df.to_pickle(os.path.join(out_dir, f"{save_name}.pkl"))

            end_time = datetime.now()
            elapsed = (end_time - start_time)/timedelta(minutes=1)
            if elapsed < 120:
                logger.info(f"Total elapsed time: {elapsed:.1f} minutes")
            else:
                logger.info(f"Total elapsed time: {elapsed/60:.2f} hours")

            # Don't close logger process until the end
            log_queue.put_nowait(None)
            lp.get()

