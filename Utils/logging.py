import logging


def get_logger():
    logger = logging.getLogger('log')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    return logger
