#!/usr/bin/python3

# handlers.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import logging
from collections import namedtuple
from pathlib import Path
from typing import List
from zipfile import ZipFile

from eds4jinja2.builders.report_builder import ReportBuilder
from eds4jinja2.builders.report_builder_actions import make_pdf_from_latex, copy_static_content

from lam4doc.config import config, HTML_REPORT_TYPE, PDF_REPORT_TYPE

logger = logging.getLogger(config.LAM_LOGGER)

FileInfo = namedtuple('FileInfo', 'location file_name')
IndexInfo = namedtuple('IndexInfo', 'name, config_location')


class ReportTypeError(Exception):
    """
        An exception when no acceptable template location has been found.
    """


def get_report_location(extension: str) -> str:
    if extension == HTML_REPORT_TYPE:
        return config.LAM_HTML_REPORT_TEMPLATE_LOCATION
    elif extension == PDF_REPORT_TYPE:
        return config.LAM_PDF_REPORT_TEMPLATE_LOCATION
    raise ReportTypeError('No acceptable report template location found')


def generate_report(location: str, report_builder: ReportBuilder, report_name: str = None) -> Path:
    """
    Handler for generating the lam report.
    :param location: path to the report templates
    :param report_builder: a report builder type service (eds4jinja2.builders.report_builder.ReportBuilder)
    :param report_name: optional name for the report
    :return: location of the report document
    """
    logger.debug(f'start service for generating report with location: {location}')

    report_builder.make_document()

    report_path = Path(str(location)) / (report_name if report_name else report_builder.template)

    logger.debug(f'finish service for generating report with location: {location}')
    return report_path


def build_report_for_html(additional_config: dict, location: str, extension: str) -> FileInfo:
    report_builder = ReportBuilder(target_path=get_report_location(extension),
                                   output_path=location,
                                   additional_config=additional_config)
    return FileInfo(generate_report(location, report_builder), 'report.html')


def build_report_for_pdf(additional_config: dict, location: str, extension: str) -> FileInfo:
    report_locations = list()
    for filename in config.LAM_PDF_REPORT_TEMPLATE_LATEX_FILES:
        additional_config['template'] = filename
        additional_config["latex_engine"] = "xelatex"
        report_builder = ReportBuilder(target_path=get_report_location(extension),
                                       output_path=location,
                                       additional_config=additional_config)
        report_builder.add_before_rendering_listener(copy_static_content)
        report_builder.add_after_rendering_listener(make_pdf_from_latex)

        report_locations.append(FileInfo(generate_report(location, report_builder, filename.replace('tex', 'pdf')),
                                         filename.replace('tex', 'pdf')))

    return FileInfo(zip_files(location, report_locations, 'report.zip'), 'report.zip')


def generate_lam_report(location: str, extension: str) -> FileInfo:
    """
    Method for generating the lam report using the generic prepare_template and generate_report
    :param extension: definition for eds4jinja2 report output type
    :param location: path to the report templates
    :return: path to report
    """
    logger.debug(f'start service for generating lam report with {extension} extension')

    additional_config = {
        "conf": {
            "default_endpoint": config.LAM_FUSEKI_REPORT_URL
        }
    }

    report = None
    if extension == HTML_REPORT_TYPE:
        report = build_report_for_html(additional_config, location, extension)
    elif extension == PDF_REPORT_TYPE:
        report = build_report_for_pdf(additional_config, location, extension)

    logger.debug('finish service for generating lam report')
    return report


def generate_indexes(location: str) -> List[FileInfo]:
    """
    Method for generating the lam indexes and zipping them using the generic prepare_template and generate_report
    :param location: path to where to create the reports
    :return: list of indexes as FileInfo tuples
    """
    logger.debug('start service for generating lam indexes')

    index_info = [IndexInfo('celex', config.LAM_CELEX_CONFIG_NAME),
                  IndexInfo('classes', config.LAM_CLASSES_CONFIG_NAME),
                  IndexInfo('properties', config.LAM_PROPERTIES_CONFIG_NAME)]
    index_files_info = list()

    for index in index_info:
        logger.debug(f'create report for {index.name}, with config {index.config_location}')
        index_location = Path(location) / index.name
        index_location.mkdir()
        report_builder = ReportBuilder(target_path=config.LAM_INDEXES_TEMPLATE_LOCATION,
                                       config_file=index.config_location,
                                       output_path=index_location,
                                       additional_config={"conf": {"endpoint": config.LAM_FUSEKI_REPORT_URL}})
        index_files_info.append(FileInfo(location=generate_report(index_location, report_builder),
                                         file_name=f'{index.name}.json'))

    logger.debug('finish service for generating lam indexes')
    return index_files_info


def zip_files(location: str, files: List[FileInfo], zip_name: str = None) -> Path:
    """
    Method for zipping a list of files using the FileInfo tuple as info about the files.
    :param location: location of the archive to be created
    :param files: list of FileInfo tuples of files to be zipped
    :param zip_name: name of the archive, defaults to 'archive.zip'
    :return: path to the created archive
    """
    logger.debug(f'start zipping {", ".join([file.file_name for file in files])} in {location}.')
    if not zip_name:
        zip_name = 'archive.zip'

    zip_path = Path(location) / zip_name
    with ZipFile(zip_path, 'w') as zip_report:
        for file_info in files:
            logger.debug(f'zipping {file_info.file_name}.')
            zip_report.write(file_info.location, file_info.file_name)

    logger.debug(f'finish zipping {", ".join([file.file_name for file in files])} in {location}.')
    return zip_path
