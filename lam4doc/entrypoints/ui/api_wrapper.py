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

from lam4doc import config
from lam4doc.config import LAM_LOGGER

logger = logging.getLogger(LAM_LOGGER)


def get_lam_report() -> tuple:
    """
    Method to connect to the lam api to get the report
    :return: html report
    :rtype: file, int
    """
    logger.debug('start get report api call')
    try:
        response = requests.get(url=config.LAM_API_SERVICE + '/generate-report', timeout=config.LAM_DEFAULT_TIMEOUT)
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
