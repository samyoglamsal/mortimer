import logging
import sys

def create_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s [%(module)s:%(funcName)s:%(lineno)d] %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger