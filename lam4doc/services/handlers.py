#!/usr/bin/python3

# handlers.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import logging
from pathlib import Path
from typing import List
from zipfile import ZipFile

from eds4jinja2.builders.report_builder import ReportBuilder

from lam4doc import config
from lam4doc.config import LAM_LOGGER
from lam4doc.services.helpers import FileInfo, IndexInfo

logger = logging.getLogger(LAM_LOGGER)


def generate_report(target_location: str, report_builder: ReportBuilder) -> Path:
    """
    Handler for generating the lam report.
    :param target_location: path to the report templates
    :param report_builder: a report builder type service (eds4jinja2.builders.report_builder.ReportBuilder)
    :return: location of the report document
    """
    logger.debug(f'start service for generating report with target_location: {target_location}')

    report_builder.make_document()

    report_path = Path(str(target_location)) / report_builder.template

    logger.debug(f'finish service for generating report with target_location: {target_location}')
    return report_path


def generate_lam_report(target_location: str) -> Path:
    """
    Method for generating the lam report using the generic prepare_template and generate_report
    :param target_location: path to the report templates
    :return: path to report
    """
    logger.debug('start service for generating lam report')

    report_builder = ReportBuilder(target_path=config.LAM_REPORT_TEMPLATE_LOCATION,
                                   output_path=target_location,
                                   additional_config={"conf": {"default_endpoint": config.LAM_FUSEKI_SERVICE}})
    report_location = generate_report(target_location, report_builder)

    logger.debug('finish service for generating lam report')
    return report_location


def generate_indexes(target_location: str) -> List[FileInfo]:
    """
    Method for generating the lam indexes and zipping them using the generic prepare_template and generate_report
    :param target_location: path to where to create the reports
    :return: list of indexes as FileInfo tuples
    """
    logger.debug('start service for generating lam indexes')

    index_info = [IndexInfo('celex', config.LAM_CELEX_CONFIG_NAME),
                  IndexInfo('classes', config.LAM_CLASSES_CONFIG_NAME),
                  IndexInfo('properties', config.LAM_PROPERTIES_CONFIG_NAME)]
    index_files_info = list()

    for index in index_info:
        logger.debug(f'create report for {index.name}, with config {index.config_location}')
        index_target_location = Path(target_location) / index.name
        index_target_location.mkdir()
        report_builder = ReportBuilder(target_path=config.LAM_INDEXES_TEMPLATE_LOCATION,
                                       config_file=index.config_location,
                                       output_path=index_target_location,
                                       additional_config={"conf": {"endpoint": config.LAM_FUSEKI_SERVICE}})
        index_files_info.append(FileInfo(location=generate_report(index_target_location, report_builder),
                                         file_name=f'{index.name}.json'))

    logger.debug('finish service for generating lam indexes')
    return index_files_info


def zip_files(target_location: str, files: List[FileInfo], zip_name: str = None) -> Path:
    """
    Method for zipping a list of files using the FileInfo tuple as info about the files.
    :param target_location: location of the archive to be created
    :param files: list of FileInfo tuples of files to be zipped
    :param zip_name: name of the archive, defaults to 'archive.zip'
    :return: path to the created archive
    """
    logger.debug(f'start zipping {", ".join([file.file_name for file in files])} in {target_location}.')
    if not zip_name:
        zip_name = 'archive.zip'

    zip_path = Path(target_location) / zip_name
    with ZipFile(zip_path, 'w') as zip_report:
        for file_info in files:
            logger.debug(f'zipping {file_info.file_name}.')
            zip_report.write(file_info.location, file_info.file_name)

    logger.debug(f'finish zipping {", ".join([file.file_name for file in files])} in {target_location}.')
    return zip_path
