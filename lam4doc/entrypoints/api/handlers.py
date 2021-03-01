#!/usr/bin/python3

# handlers.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
OpenAPI method handlers.
"""
import logging
import tempfile
from pathlib import Path

import requests
from flask import send_file
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import InternalServerError, UnprocessableEntity, BadRequest

from lam4doc.adapters.sparql_adapter import FusekiSPARQLAdapter
from lam4doc.config import config, DEFAULT_REPORT_TYPE, REPORT_EXTENSIONS, HTML_REPORT_TYPE, PDF_REPORT_TYPE
from lam4doc.services.handlers import generate_lam_report as service_generate_lam_report, \
    generate_indexes as service_generate_indexes, zip_files

logger = logging.getLogger(config.LAM_LOGGER)


def generate_lam_report(report_extension: str = DEFAULT_REPORT_TYPE) -> tuple:
    """
    API method for generating and requesting a lam report.
    :rtype: report file (html), int
    :return: the lam report
    """
    logger.debug('start generate lam report endpoint')

    if report_extension not in REPORT_EXTENSIONS:
        exception_text = 'Wrong report_extension format. Accepted formats: ' \
                         f'{", ".join([format for format in REPORT_EXTENSIONS])}'
        logger.exception(exception_text)
        raise UnprocessableEntity(exception_text)  # 422

    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            report_file_info = service_generate_lam_report(temp_folder, report_extension)

            logger.debug('finish generate lam report endpoint')
            return send_file(report_file_info.location, attachment_filename=report_file_info.file_name,
                             as_attachment=True)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500


def generate_indexes() -> tuple:
    """
    API method for generating and requesting the LAM indexes.
    :rtype: report file (zip), int
    :return: the lam indexes
    """
    logger.debug('start generate lam indexes endpoint')
    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            index_files_info = service_generate_indexes(temp_folder)
            archive = zip_files(temp_folder, index_files_info, config.LAM_INDEXES_ZIP_NAME)

            logger.debug('finish generate lam indexes endpoint')
            return send_file(archive, as_attachment=True)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500


def get_lam_files() -> tuple:
    """
    API method for generating and requesting all LAM files.
    :rtype: report file (zip), int
    :return: all lam files: HTML and PDF report, and 3 index files
    """
    logger.debug('start get lam files endpoint')
    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            files_to_zip = list()
            files_to_zip.append(service_generate_lam_report(temp_folder, HTML_REPORT_TYPE))
            files_to_zip.append(service_generate_lam_report(temp_folder, PDF_REPORT_TYPE))
            files_to_zip += service_generate_indexes(temp_folder)

            archive = zip_files(temp_folder, files_to_zip, config.LAM_ALL_ZIP_NAME)

            logger.debug('finish get lam files endpoint')
            return send_file(archive, as_attachment=True)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500


def upload_rdfs(body: dict, lam_properties_document: FileStorage = None, lam_classes_document: FileStorage = None,
                celex_classes_document: FileStorage = None) -> tuple:
    """
    API method for uploading 3 RDF files.
    :return: nothing
    """
    logger.debug('Entering upload_rdfs')

    if not lam_properties_document and not lam_classes_document and not celex_classes_document:
        logger.error("No file was specified. Returning 400.")
        raise BadRequest("Please supply at least one file: lam_properties_document, lam_classes_document, "
                         "celex_classes_document")

    dataset_name = body.get("dataset_name")
    try:
        logger.debug(body)
        sparql_adapter = FusekiSPARQLAdapter(config.LAM_FUSEKI_SERVICE, requests)

        with tempfile.TemporaryDirectory() as temp_folder:
            if lam_properties_document:
                local_lam_properties_file = Path(temp_folder) / lam_properties_document.filename
                lam_properties_document.save(local_lam_properties_file)
                logger.info("lam_properties_document - saved to " + str(local_lam_properties_file))
                if not sparql_adapter.delete_graph(dataset_name, config.LAM_DOCUMENT_PROPERTY_GRAPH):
                    sparql_adapter.create_dataset(dataset_name)
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    config.LAM_DOCUMENT_PROPERTY_GRAPH,
                                                    str(local_lam_properties_file))

            if lam_classes_document:
                local_lam_classes_file = Path(temp_folder) / lam_classes_document.filename
                lam_classes_document.save(local_lam_classes_file)
                logger.info("lam_classes_document - saved to " + str(local_lam_classes_file))
                sparql_adapter.delete_graph(dataset_name, config.LAM_CLASSES_GRAPH)
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    config.LAM_CLASSES_GRAPH,
                                                    str(local_lam_classes_file))

            if celex_classes_document:
                local_celex_classes_file = Path(temp_folder) / celex_classes_document.filename
                celex_classes_document.save(local_celex_classes_file)
                logger.info("lam_properties_document - saved to " + str(local_celex_classes_file))
                sparql_adapter.delete_graph(dataset_name, config.LAM_CELEX_CLASSES_GRAPH)
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    config.LAM_CELEX_CLASSES_GRAPH,
                                                    str(local_celex_classes_file))

            return 'OK', 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500
    finally:
        logger.debug('Exiting upload_rdfs')
