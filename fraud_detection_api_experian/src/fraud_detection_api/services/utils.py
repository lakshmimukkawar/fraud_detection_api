import logging
import sys


def get_logger(name: str):
    """
    Function for defining logger settings with particular format

    Parameters:
        name(str): string

    Returns:
    logger: Returns logger object
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)-4s - %(levelname)-6s - %(message)s"
    )
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    logger = logging.getLogger(name)
    return logger
