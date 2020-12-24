#!/usr/bin/python3

# helpers.py
# Date:  23/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import logging
from json import loads
from pathlib import Path

from lam4doc import config
from lam4doc.config import LAM_LOGGER

logger = logging.getLogger(LAM_LOGGER)


def generate_report_builder_config(config_path: str) -> dict:
    """
    Helper method for updating the config from the report template
    :param config_path: path to the config file
    :return: configuration dictionary
    """
    logger.debug(f'start with config path: {config_path}')
    logger.debug(f'default endpoint: {config.LAM_FUSEKI_SERVICE}')

    config_dict = loads(Path(config_path).read_bytes())
    config_dict["conf"]["default_endpoint"] = config.LAM_FUSEKI_SERVICE

    logger.debug(f'finish with config path: {config_path}')
    return config_dict
