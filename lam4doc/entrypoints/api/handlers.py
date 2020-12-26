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
from lam4doc.config import LAM_LOGGER
from lam4doc.services.handlers import generate_lam_report as service_generate_lam_report, prepare_report_template

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
            prepare_report_template(temp_folder)
            report_builder = ReportBuilder(target_path=temp_folder)
            report_location = service_generate_lam_report(temp_folder, report_builder)

            logger.debug('finish generate lam report endpoint')
            return send_file(report_location, as_attachment=True)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500


def upload_rdfs(lam_properties_document: FileStorage = None, lam_classes_document: FileStorage = None,
                celex_classes_document: FileStorage = None) -> tuple:
    """
    API method for uploading 3 RDF files.
    :return: nothing
    """
    logger.debug('Entering upload_rdfs')

    dataset_name = "A_DATASET_NAME"

    try:
        sparql_adapter = FusekiSPARQLAdapter("http://fuseki:3030/", requests)

        if lam_properties_document is None and lam_classes_document is None and celex_classes_document is None:
            logger.error("No file was specified. Returning 400.")
            return "Please supply at least one file: lam_properties_document, lam_classes_document, " \
                   "celex_classes_document", 400

        with tempfile.TemporaryDirectory() as temp_folder:
            if lam_properties_document:
                local_lam_properties_file = Path(temp_folder) / lam_properties_document.filename
                lam_properties_document.save(local_lam_properties_file)
                logger.info("lam_properties_document - saved to " + str(local_lam_properties_file))
                sparql_adapter.delete_graph(dataset_name, "<http://publications.europa.eu/resources/authority/lam/DocumentProperty>")
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    "http://publications.europa.eu/resources/authority/lam/DocumentProperty",
                                                    str(local_lam_properties_file))

            if lam_classes_document:
                local_lam_classes_file = Path(temp_folder) / lam_classes_document.filename
                lam_classes_document.save(local_lam_classes_file)
                logger.info("lam_classes_document - saved to " + local_lam_classes_file)
                sparql_adapter.delete_graph(dataset_name,
                                            "<http://publications.europa.eu/resources/authority/lam/LAMLegalDocument>")
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    "http://publications.europa.eu/resources/authority/lam/LAMLegalDocument",
                                                    str(local_lam_classes_file))

            if celex_classes_document:
                local_celex_classes_file = Path(temp_folder) / celex_classes_document.filename
                celex_classes_document.save(local_celex_classes_file)
                logger.info("lam_properties_document - saved to " + local_celex_classes_file)
                sparql_adapter.delete_graph(dataset_name,
                                            "<http://publications.europa.eu/resources/authority/celex/CelexLegalDocument>")
                sparql_adapter.upload_file_to_graph(dataset_name,
                                                    "http://publications.europa.eu/resources/authority/celex/CelexLegalDocument",
                                                    str(local_celex_classes_file))

            return 'OK', 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500
    finally:
        logger.debug('Exiting upload_rdfs')
