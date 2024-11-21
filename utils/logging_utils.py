import logging

def setup_logger(level=logging.INFO):
    """
    Configures the root logger with a specified logging level and format.

    This function sets up the logging configuration, including the log message format, 
    date/time format, and the desired log level for the root logger.

    :param level: The logging level to use. Default is logging.INFO.
                  Other common levels include logging.DEBUG, logging.WARNING, 
                  logging.ERROR, and logging.CRITICAL.
    :return: None
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger().setLevel(level)
