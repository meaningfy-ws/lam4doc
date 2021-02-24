#!/usr/bin/python3

# api_wrapper.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
Service to consume validator API.
"""
import logging

import requests
from requests import Timeout
from werkzeug.datastructures import FileStorage

from lam4doc.config import config

logger = logging.getLogger(config.LAM_LOGGER)


def get_lam_report(report_extension: str) -> tuple:
    """
    Method to connect to the lam api to get the report
    :type report_extension: report extension type
    :return: html report
    :rtype: file, int
    """
    logger.debug(f'start get report api call with {report_extension} format')
    try:
        response = requests.get(url=config.LAM_API_SERVICE + '/generate-report',
                                params={'report_extension': report_extension},
                                timeout=config.LAM_DEFAULT_TIMEOUT)
    except Timeout as exception:
        logger.exception(str(exception))

    logger.debug('finish get report api call')
    return response.content, response.status_code


def get_indexes() -> tuple:
    """
    Method to connect to the lam api to get the indexes
    :return: zip file
    :rtype: file, int
    """
    logger.debug('start get indexes api call')
    try:
        response = requests.get(url=config.LAM_API_SERVICE + '/generate-indexes', timeout=config.LAM_DEFAULT_TIMEOUT)
    except Timeout as exception:
        logger.exception(str(exception))

    logger.debug('finish get indexes api call')
    return response.content, response.status_code


def get_lam_files() -> tuple:
    """
    Method to connect to the lam api to get all LAM files
    :return: zip file
    :rtype: file, int
    """
    logger.debug('start get all lam files api call')
    try:
        response = requests.get(url=config.LAM_API_SERVICE + '/lam-files', timeout=config.LAM_DEFAULT_TIMEOUT)
    except Timeout as exception:
        logger.exception(str(exception))

    logger.debug('finish get all lam files api call')
    return response.content, response.status_code


def upload_rdf(lam_properties_document: FileStorage, lam_classes_document: FileStorage,
               celex_classes_document: FileStorage, dataset_name: str) -> tuple:
    """
    Method to connect to the lam api to upload LAM RDF files
    :param lam_properties_document:
    :param lam_classes_document:
    :param celex_classes_document:
    :param dataset_name: name of the dataset for the files to be uploaded to
    :return:
    """
    data = {
        'dataset_name': dataset_name,
    }

    lam_properties_document = (lam_properties_document.filename, lam_properties_document.stream,
                               lam_properties_document.mimetype) if lam_properties_document else None
    lam_classes_document = (lam_classes_document.filename, lam_classes_document.stream,
                            lam_classes_document.mimetype) if lam_classes_document else None
    celex_classes_document = (celex_classes_document.filename, celex_classes_document.stream,
                              celex_classes_document.mimetype) if celex_classes_document else None

    files = {
        'lam_properties_document': lam_properties_document,
        'lam_classes_document': lam_classes_document,
        'celex_classes_document': celex_classes_document
    }

    response = requests.post(config.LAM_API_SERVICE + '/upload-rdf', data=data, files=files)
    return response.content, response.status_code
