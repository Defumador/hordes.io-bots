import logging

# custom logger
logger = logging.getLogger('hordes.io')

def logger_init(debug: bool = False):
    """
    Logging levels:
        - Critical: None
        - Error: Program errors
        - Warning: Missing requirements
        - Info: Information of the program
        - Debug: workflow
    :return: void
    """
    global logger
    if debug:
        level = logging.DEBUG  # 10 basic
    else:
        level = logging.INFO  # 20
    logging.basicConfig(level=level, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger('hordes.io')
    # File handler
    file_handler = logging.FileHandler('hordes.io.log')
    file_handler.setLevel(logging.ERROR)
    file_formatter = logging.Formatter('[%(asctime)s][%(filename)s][%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    logger.info('Setting logger...')
