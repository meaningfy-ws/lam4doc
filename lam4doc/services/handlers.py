#!/usr/bin/python3

# handlers.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import logging
from json import dumps
from pathlib import Path
from shutil import copytree
from zipfile import ZipFile

from eds4jinja2.builders.report_builder import ReportBuilder

from lam4doc import config
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

    report_path = Path(str(target_location)) / 'output' / report_builder.template

    logger.debug(f'finish service for generating report with target_location: {target_location}')
    return report_path


def generate_lam_report(target_location: str) -> Path:
    """
    Method for generating the lam report using the generic prepare_template and generate_report
    :param target_location: path to the report templates
    :return: path to report
    """
    logger.debug('start service for generating lam report')

    prepare_template(target_location, config.LAM_REPORT_TEMPLATE_LOCATION)
    report_builder = ReportBuilder(target_path=target_location)
    report_location = generate_report(target_location, report_builder)

    logger.debug('finish service for generating lam report')
    return report_location


def generate_indexes(target_location: str) -> Path:
    """
    Method for generating the lam indexes and zipping them using the generic prepare_template and generate_report
    :param target_location: path to the report templates
    :return: path to zip
    """
    logger.debug('start service for generating lam indexes')

    logger.debug('start generation for celex')
    celex_target_location = Path(target_location) / 'celex'
    prepare_template(celex_target_location, config.LAM_INDEXES_TEMPLATE_LOCATION, config.LAM_CELEX_CONFIG)
    report_builder = ReportBuilder(target_path=celex_target_location)
    celex_index = generate_report(celex_target_location, report_builder)

    logger.debug('start generation for classes')
    classes_target_location = Path(target_location) / 'classes'
    prepare_template(classes_target_location, config.LAM_INDEXES_TEMPLATE_LOCATION, config.LAM_CLASSES_CONFIG)
    report_builder = ReportBuilder(target_path=classes_target_location)
    classes_index = generate_report(classes_target_location, report_builder)

    logger.debug('start generation for properties')
    properties_target_location = Path(target_location) / 'properties'
    prepare_template(properties_target_location, config.LAM_INDEXES_TEMPLATE_LOCATION, config.LAM_PROPERTIES_CONFIG)
    report_builder = ReportBuilder(target_path=properties_target_location)
    properties_index = generate_report(properties_target_location, report_builder)

    logger.debug('zipping indexes')
    zip_path = Path(target_location) / 'indexes.zip'
    with ZipFile(zip_path, 'w') as zip_report:
        zip_report.write(celex_index, arcname='celex.json')
        zip_report.write(classes_index, arcname='classes.json')
        zip_report.write(properties_index, arcname='properties.json')

    logger.debug('finish service for generating lam indexes')
    return zip_path
