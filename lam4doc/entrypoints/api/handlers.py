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

from eds4jinja2.builders.report_builder import ReportBuilder
from flask import send_file
from werkzeug.exceptions import InternalServerError

from lam4doc import config
from lam4doc.config import LAM_LOGGER
from lam4doc.services.handlers import generate_report as service_generate_report, prepare_template

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
            prepare_template(temp_folder, config.LAM_REPORT_TEMPLATE_LOCATION)
            report_builder = ReportBuilder(target_path=temp_folder)
            report_location = service_generate_report(temp_folder, report_builder)

            logger.debug('finish generate lam report endpoint')
            return send_file(report_location, as_attachment=True)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500
