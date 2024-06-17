"""Setup configuration."""

import configparser
import os

from src.fraud_detection_api.services.utils import get_logger


logger = get_logger(__name__)


def get_config():
    """
    Read env variable and setup config accordingly.
    """
    env_var = os.environ.get("FRAUDDETECTION_ENV", "DEFAULT")
    config = configparser.ConfigParser()
    filepath = f"{os.path.join(os.path.dirname(__file__))}/config.ini"
    logger.info(f"config file path-> {filepath}")
    config.read(f"{os.path.join(os.path.dirname(__file__))}/config.ini")
    return config[env_var]
