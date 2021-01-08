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
from json import loads
from pathlib import Path

from flask import render_template, send_from_directory, flash

from lam4doc.config import config
from lam4doc.entrypoints.ui import app
from lam4doc.entrypoints.ui.api_wrapper import get_lam_report as api_get_lam_report, get_indexes as api_get_indexes
from lam4doc.entrypoints.ui.forms import ReportTypeForm

logger = logging.getLogger(config.LAM_LOGGER)


def get_error_message_from_response(response):
    return f'Status: {loads(response).get("status")}. Title: {loads(response).get("title")}' \
           f' Detail: {loads(response).get("detail")}'


@app.route('/', methods=['GET'])
def index():
    logger.debug('request index view')
    return render_template('index.html', title='LAM index page')


@app.route('/lam-report', methods=['GET'])
def download_lam_report():
    logger.debug('request LAM report view')

    form = ReportTypeForm()

    if form.validate_on_submit():
        response, status = api_get_lam_report(form.report_extension.data)

        if status != 200:
            exception_text = get_error_message_from_response(response)
            logger.exception(exception_text)
            flash(exception_text, 'error')
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_folder:
                    file_name = f'LAM-report.{form.report_extension.data}'
                    report = Path(temp_folder) / file_name
                    report.write_bytes(response)
                    logger.debug('render LAM report view')
                    return send_from_directory(Path(temp_folder), file_name, as_attachment=True)
            except Exception as e:
                logger.exception(str(e))
                flash(str(e), 'error')

    logger.debug('render LAM report clean view')
    return render_template('report.html', form=form, title='Get LAM report')


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
