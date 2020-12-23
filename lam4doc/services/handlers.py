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

from lam4doc.config import LAM_LOGGER
from lam4doc.services.helpers import generate_report_builder_config

logger = logging.getLogger(LAM_LOGGER)


def prepare_template(target_location: str, template_location: str, config_location: str = None):
    """
    Copy report template and generate the config to the temporary directory indicated in target_location
    :param target_location: path to from where to copy the templates to be used by ReportBuilder
    :param template_location: path to the template to be used by ReportBuilder
    :param config_location: path to the config to be used by ReportBuilder, if None, the default location is used
    """
    logger.debug(f'start service for preparing: {template_location}')
    if not config_location:
        config_location = f'{template_location}/config.json'

    copytree(template_location, target_location, dirs_exist_ok=True)

    with open(Path(target_location) / 'config.json', 'w') as config_file:
        config_content = generate_report_builder_config(config_location)
        config_file.write(dumps(config_content))

    logger.debug(f'finish service for preparing: {template_location}')


def generate_report(target_location: str, report_builder: ReportBuilder) -> Path:
    """
    Handler for generating the lam report.
    :param target_location: path to the report templates
    :param report_builder: a report builder type service (eds4jinja2.builders.report_builder.ReportBuilder)
    :return: location of the report document
    """
    logger.debug(f'start service for generating report with target_location: {target_location}')

    report_builder.make_document()

    report_path = Path(str(target_location)) / 'output/main.html'

    logger.debug(f'finish service for generating report with target_location: {target_location}')
    return report_path
