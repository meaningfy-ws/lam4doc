#!/usr/bin/python3

# helpers.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
import logging
from json import loads
from pathlib import Path

from lam4doc import config
from lam4doc.config import LAM_LOGGER

logger = logging.getLogger(LAM_LOGGER)


def generate_report_builder_config():
    logger.debug(f'starting config generation with template location:  {config.LAM_REPORT_TEMPLATE_LOCATION}')
    logger.debug(f'default endpoint:  {config.LAM_FUSEKI_SERVICE}')

    config_dict = loads((Path(config.LAM_REPORT_TEMPLATE_LOCATION) / "config.json").read_bytes())
    config_dict["conf"]["default_endpoint"] = config.LAM_FUSEKI_SERVICE
    return config_dict
