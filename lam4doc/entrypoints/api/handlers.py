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
from eds4jinja2.builders.report_builder import ReportBuilder
from flask import send_file
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import InternalServerError

from lam4doc.adapters.sparql_adapter import FusekiSPARQLAdapter
from lam4doc.config import LAM_LOGGER, LAM_DOCUMENT_PROPERTY_GRAPH, LAM_CLASSES_GRAPH, LAM_CELEX_CLASSES_GRAPH, \
    LAM_FUSEKI_PORT, LAM_FUSEKI_LOCATION
from lam4doc.services.handlers import generate_lam_report as service_generate_lam_report, prepare_report_template
from lam4doc.config import LAM_LOGGER
from lam4doc.services.handlers import generate_lam_report as service_generate_lam_report, \
    generate_indexes as service_generate_indexes, zip_files

logger = logging.getLogger(LAM_LOGGER)


def generate_lam_report() -> tuple:
    """
    API method for generating and requesting a lam report.
    :rtype: report file (html), int
    :return: the lam report
    """
    logger.debug('start generate lam report endpoint')
    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            report_location = service_generate_lam_report(temp_folder)

            logger.debug('finish generate lam report endpoint')
            return send_file(report_location, as_attachment=True)  # 200
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

    dataset_name = body.get("dataset_name")
    if not dataset_name:
        logger.error("The name of the dataset is required.")
        return 'Dataset name is required', 400

    try:
        logger.debug(body)
        sparql_adapter = FusekiSPARQLAdapter(LAM_FUSEKI_LOCATION + ":" + str(LAM_FUSEKI_PORT) + "/", requests)

        if lam_properties_document is None and lam_classes_document is None and celex_classes_document is None:
            logger.error("No file was specified. Returning 400.")
            return "Please supply at least one file: lam_properties_document, lam_classes_document, " \
                   "celex_classes_document", 400

        with tempfile.TemporaryDirectory() as temp_folder:
            if lam_properties_document:
                local_lam_properties_file = Path(temp_folder) / lam_properties_document.filename
                lam_properties_document.save(local_lam_properties_file)
                logger.info("lam_properties_document - saved to " + str(local_lam_properties_file))
                sparql_adapter.delete_graph(dataset_name, "<"+ LAM_DOCUMENT_PROPERTY_GRAPH + ">")
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    LAM_DOCUMENT_PROPERTY_GRAPH,
                                                    str(local_lam_properties_file))

            if lam_classes_document:
                local_lam_classes_file = Path(temp_folder) / lam_classes_document.filename
                lam_classes_document.save(local_lam_classes_file)
                logger.info("lam_classes_document - saved to " + local_lam_classes_file)
                sparql_adapter.delete_graph(dataset_name,
                                            "<" + LAM_CLASSES_GRAPH + ">")
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    LAM_CLASSES_GRAPH,
                                                    str(local_lam_classes_file))

            if celex_classes_document:
                local_celex_classes_file = Path(temp_folder) / celex_classes_document.filename
                celex_classes_document.save(local_celex_classes_file)
                logger.info("lam_properties_document - saved to " + local_celex_classes_file)
                sparql_adapter.delete_graph(dataset_name,
                                            "<" + LAM_CELEX_CLASSES_GRAPH + ">")
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    LAM_CELEX_CLASSES_GRAPH,
                                                    str(local_celex_classes_file))

            return 'OK', 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500
    finally:
        logger.debug('Exiting upload_rdfs')


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
            archive = zip_files(temp_folder, index_files_info, 'indexes.zip')

            logger.debug('finish generate lam indexes endpoint')
            return send_file(archive, as_attachment=True)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500
