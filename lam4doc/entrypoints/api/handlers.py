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

from flask import send_file
from werkzeug.exceptions import InternalServerError

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
