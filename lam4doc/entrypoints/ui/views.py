#!/usr/bin/python3

# views.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
UI pages
"""
import logging
import tempfile
from pathlib import Path

from flask import render_template, send_from_directory, flash

from lam4doc.config import LAM_LOGGER
from lam4doc.entrypoints.ui import app
from lam4doc.entrypoints.ui.api_wrapper import get_lam_report as api_get_lam_report, get_indexes as api_get_indexes

logger = logging.getLogger(LAM_LOGGER)


@app.route('/', methods=['GET'])
def index():
    logger.debug('request index view')
    return render_template('index.html', title='LAM index page')


@app.route('/lam-report', methods=['GET'])
def download_lam_report():
    logger.debug('request LAM report view')
    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            file_name = 'LAM-report.html'
            report_content, _ = api_get_lam_report()
            report = Path(temp_folder) / file_name
            report.write_bytes(report_content)
            logger.debug('render LAM report view')
            return send_from_directory(Path(temp_folder), file_name, as_attachment=True)
    except Exception as e:
        logger.exception(str(e))
        flash(str(e), 'error')

    logger.debug('redirect to index view')
    return render_template('index.html')


@app.route('/indexes-report', methods=['GET'])
def download_indexes():
    logger.debug('request LAM indexes view')
    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            file_name = 'indexes.zip'
            report_content, _ = api_get_indexes()
            report = Path(temp_folder) / file_name
            report.write_bytes(report_content)
            logger.debug('render LAM indexes view')
            return send_from_directory(Path(temp_folder), file_name, as_attachment=True)
    except Exception as e:
        logger.exception(str(e))
        flash(str(e), 'error')

    logger.debug('redirect to index view')
    return render_template('index.html')
