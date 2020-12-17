#!/usr/bin/python3

# handlers.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

""" """
import logging
from json import dumps
from pathlib import Path
from shutil import copytree

from eds4jinja2.builders.report_builder import ReportBuilder

from lam4doc import config
from lam4doc.config import LAM_LOGGER
from lam4doc.entrypoints.api.helpers import generate_report_builder_config

logger = logging.getLogger(LAM_LOGGER)


def generate_lam_report(target_location: str) -> Path:
    """
    Handler for generating the lam report.
    :param target_location: path to from where to copy the templates to be used by ReportBuilder
    :return: target_location of the report document
    """
    logger.debug('start service for generating lam report ')

    template_location = config.LAM_REPORT_TEMPLATE_LOCATION
    logger.debug(f'template location {template_location}')

    copytree(template_location, target_location, dirs_exist_ok=True)

    with open(Path(target_location) / 'config.json', 'w') as config_file:
        config_content = generate_report_builder_config()
        config_file.write(dumps(config_content))

    report_builder = ReportBuilder(target_path=target_location)
    report_builder.make_document()

    report_path = Path(str(target_location)) / 'output/main.html'

    logger.debug('finish service for generating lam report ')
    return report_path
