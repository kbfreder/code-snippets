
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
    msg_fmt = '%(asctime)s - %(filename)s - %(message)s'
    date_fmt = '%Y-%m-%d %H:%M'

    basic_format = {'format': msg_fmt, 'datefmt': date_fmt}
    fmtr_format = {'fmt': msg_fmt, 'datefmt': date_fmt}

    logging.basicConfig(level=log_level, **basic_format)
    logger = logging.getLogger(logger_name)

    if log_file_path:
        f_handler = logging.FileHandler(log_file_path)
        f_handler.setLevel(log_file_level)
        f_handler.setFormatter(logging.Formatter(**fmtr_format))
        logger.addHandler(f_handler)

    return logger