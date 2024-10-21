
import logging
from logging.handlers import QueueHandler

# just to mock up some "work"
from time import sleep
from random import random

from mp_config import LOGGER_NAME



def extract_text_from_ticket_mp(input, queue):

    # get logger & add queue handler
    logger = logging.getLogger(LOGGER_NAME)
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)

    # opreate on the input
    output = input * input
    sleep(random())

    # return the output
    return output
