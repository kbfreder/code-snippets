
import logging


def configure_logger(
        logger_name: str,
        log_level: int = 20, # INFO
        log_file_path=None,
        log_file_level=10 # DEBUG
    ):
    """Configures a python logger object.

    Logging messages will be sent to stdout and optionally to a file.
    A different logging level can be configured between the two 
    destinations.

    Note levels should be supplied as int's or logging.XXX level objects

    params:
    ----------
    logger_name (str): name of logger
    log_level (int): logging level for stdout. Default = 20, which is INFO.
    log_file (None or str): file path for the logging file. Default is None,
        which will not create a logging file handler. 
    log_file_level (int): logging level for file. Default = 10, which is DEBUG.

    returns:
    --------
    logging.Logger object
    """
    # logging formatting
    stdout_msg_fmt = '%(asctime)s - %(message)s'
    file_msg_fmt = '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'

    date_fmt = '%Y-%m-%d %H:%M'

    # basic_format = {'format': msg_fmt, 'datefmt': date_fmt}
    stdout_fmtr = {'fmt': stdout_msg_fmt, 'datefmt': date_fmt}
    file_fmtr = {'fmt': file_msg_fmt, 'datefmt': date_fmt}

    # logging.basicConfig(level=log_level, **basic_format)
    logger = logging.getLogger(logger_name)
    logger.setLevel(min(log_level, log_file_level))

    # create STDOUT handler
    s_handler = logging.StreamHandler()
    s_handler.setLevel(log_level)
    s_handler.setFormatter(logging.Formatter(**stdout_fmtr))
    logger.addHandler(s_handler)

    if log_file_path:
        f_handler = logging.FileHandler(log_file_path)
        f_handler.setLevel(log_file_level)
        f_handler.setFormatter(logging.Formatter(**file_fmtr))
        logger.addHandler(f_handler)

    return logger

# usage

logger = configure_logger(
    'loggy-mc-logger',
    log_file_path="./logs/test.txt",
    log_file_level=10
)

logger.debug("Test message - DEBUG")
logger.info("Test message - INFO")
