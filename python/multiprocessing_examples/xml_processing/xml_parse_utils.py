
import os
import psutil
import pandas as pd
from collections import Counter
from datetime import datetime, timedelta
import logging
from logging.handlers import QueueHandler

from .data_parse_utils import (
    parse_email_text, 
    parse_html,
    get_text_from_attachment_data
)
from .config import DATE_FMT, LOGGER_NAME, MAX_ATTACHMENT_SIZE_MB



# NOTE:
# Rather than passing `logger` object to helper functions (e.g. `_get_attachment_data`),
# I made the decision to capture errors in `ticket_output` vs in logger messages

def extract_text_from_ticket_mp(p_dict, queue):

    # get logger & add queue handler
    logger = logging.getLogger(LOGGER_NAME)
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)

    start = datetime.now()
    p_i = p_dict['parent_idx']
    logger.debug(f"Starting ticket tag index {p_i} at {start.strftime(DATE_FMT)} - CPU usage: {psutil.cpu_percent(interval=1)} - number of sub-items: {p_dict['num_children']}")
    
    ticket_num = p_dict['ticket_number']
    
    # seed trackers
    ticket_output = []
    sys_id = ''
    data_parts = []
    attachment_dict = {}
    file_ext = ''
    content_type = ''
    total_size_mb = 0

    for child_info in p_dict['child_info']:
        c_df = child_info['df']            
        
        if child_info['tag'] == 'sys_journal_field':
            item_dict = parse_journal_field(c_df)
            item_dict['ticket_number'] = ticket_num
            item_dict['item_index'] = int(child_info['idx'])
            ticket_output.append(item_dict)
    
        if child_info['tag'] == 'sys_attachment':
            if sys_id != '': # means this isn't the first attachment
                attachment_dict = _get_attachment_data(
                    data_parts, file_ext, content_type, attachment_dict
                    )
                ticket_output.append(attachment_dict)
            
            # reset/seed trackers
            sys_id = c_df.loc['sys_id', 'text']
            data_parts = []
            file_name = c_df.loc['file_name', 'text']
            if file_name is not None:
                file_ext = os.path.splitext(file_name)[-1].lower()
            else:
                file_ext = None
            content_type = c_df.loc['content_type', 'text']
            size_mb = int(c_df.loc['size_bytes', 'text']) / 1e6

            attachment_dict = {
                'ticket_number': ticket_num,
                'item_index': int(child_info['idx']),
                'datetime': c_df.loc['sys_created_on', 'text'],
                'type': child_info['tag'],
                'subtype': file_ext,
                'content_type': content_type,
                'created_by': c_df.loc['sys_created_by', 'text'],
                'filename': file_name,
                'size_mb': size_mb
            }
            total_size_mb += size_mb

            for a_info in child_info['attachment_info']:
                a_df = a_info['df']
                data_parts.append(a_df.loc['data', 'text'])
    
    # log last attachment (if there was one)
    if sys_id != '':
        attachment_dict = _get_attachment_data(
            data_parts, file_ext, content_type, attachment_dict
            )
        ticket_output.append(attachment_dict)
    
    end = datetime.now()
    elapsed = (end - start)/timedelta(minutes=1)
    print_msg = f"Finished ticket tag index {p_i} - total attachments size {total_size_mb:.2f} MB - in {elapsed:.2f} minutes"
    logger.debug(print_msg)
    
    return ticket_output