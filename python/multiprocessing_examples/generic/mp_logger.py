import logging


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