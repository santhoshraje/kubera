import logging
import sys


# logging function
def get_logger():
    logger = logging.getLogger('log')
    logger.addHandler(logging.FileHandler("Logs/debug.txt"))
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    return logger
