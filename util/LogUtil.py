import logging
import sys
import os
import time

LOG_FILE_DIR = os.path.abspath(os.path.join('results', time.strftime("%Y%m%d-%H%M%S")))

FILE_LOGGER = {}
STDOUT_LOGGER = {}


def __create_file_logger(class_name, file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.FileHandler(filename=file_name, encoding='utf-8')
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(class_name)
    logger.addHandler(screen_handler)
    logger.setLevel(logging.DEBUG)

    return logger


def __create_stdout_logger(class_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(class_name)
    logger.addHandler(screen_handler)
    logger.setLevel(logging.DEBUG)

    return logger


def get_file_logger(class_name):
    if os.path.exists(LOG_FILE_DIR) is False:
        os.makedirs(LOG_FILE_DIR)
    if FILE_LOGGER.__contains__(class_name):
        return FILE_LOGGER.get(class_name)

    file_name = os.path.join(LOG_FILE_DIR, class_name)
    logger = __create_file_logger(class_name, file_name)
    FILE_LOGGER[class_name] = logger
    return FILE_LOGGER.get(class_name)


def get_stdout_logger(class_name):
    if STDOUT_LOGGER.__contains__(class_name):
        return STDOUT_LOGGER.get(class_name)

    logger = __create_stdout_logger(class_name)
    STDOUT_LOGGER[class_name] = logger
    return STDOUT_LOGGER.get(class_name)
