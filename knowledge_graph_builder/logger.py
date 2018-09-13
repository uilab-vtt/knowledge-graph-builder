import logging

logger = None

def init_logger():
    global logger
    logger = logging.getLogger('builder_main')
    logging.getLogger('builder_main')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('main.log')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

init_logger()