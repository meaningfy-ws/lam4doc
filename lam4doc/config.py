#!/usr/bin/python3

# config.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
Project wide configuration file.
"""
import logging
import os
from pathlib import Path

HTML_REPORT_TYPE = 'html'
PDF_REPORT_TYPE = 'pdf'
DEFAULT_REPORT_TYPE = HTML_REPORT_TYPE
REPORT_EXTENSIONS = [HTML_REPORT_TYPE, PDF_REPORT_TYPE]


class LAMConfig:
    logger_name = 'lam'
    logger = logging.getLogger(logger_name)

    @property
    def LAM_LOGGER(cls) -> str:
        value = cls.logger_name
        cls.logger.debug(value)
        return value

    @property
    def LAM_DEBUG(cls) -> str:
        value = os.environ.get('LAM_DEBUG', True)
        cls.logger.debug(value)
        return value

    @property
    def LAM_FLASK_SECRET_KEY(cls) -> str:
        value = os.environ.get('LAM_FLASK_SECRET_KEY', 'secret key')
        cls.logger.debug(value)
        return value

    @property
    def LAM_API_SERVICE(cls) -> str:
        location = os.environ.get('LAM_API_LOCATION', 'http://lam-api')
        port = os.environ.get('LAM_API_PORT', 4050)
        value = f'{location}:{port}'
        cls.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_SERVICE(cls) -> str:
        location = os.environ.get('LAM_FUSEKI_LOCATION', 'http://fuseki')
        port = os.environ.get('LAM_FUSEKI_PORT', 3030)
        value = f'{location}:{port}'
        cls.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_REPORT_URL(cls) -> str:
        location = os.environ.get('LAM_FUSEKI_LOCATION', 'http://fuseki')
        port = os.environ.get('LAM_FUSEKI_PORT', 3030)
        query_url = os.environ.get('LAM_FUSEKI_QUERY_URL', '/lam/query')
        value = f'{location}:{port}{query_url}'
        cls.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_USERNAME(cls) -> str:
        value = os.environ.get('LAM_FUSEKI_USERNAME', 'admin')
        cls.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_PASSWORD(cls) -> str:
        value = os.environ.get('LAM_FUSEKI_PASSWORD', 'admin')
        cls.logger.debug(value)
        return value

    @property
    def LAM_HTML_REPORT_TEMPLATE_LOCATION(cls) -> str:
        value = str(Path(__file__).parents[1] / 'templates/html')
        cls.logger.debug(value)
        return value

    @property
    def LAM_PDF_REPORT_TEMPLATE_LOCATION(cls) -> str:
        # correct value will be used when pdf implementation is ready
        value = str(Path(__file__).parents[1] / 'templates/html')
        cls.logger.debug(value)
        return value

    @property
    def LAM_INDEXES_TEMPLATE_LOCATION(cls) -> str:
        value = str(Path(__file__).parents[1] / 'templates/indexes')
        cls.logger.debug(value)
        return value

    @property
    def LAM_CELEX_CONFIG_NAME(cls) -> str:
        value = 'celex.json'
        cls.logger.debug(value)
        return value

    @property
    def LAM_CLASSES_CONFIG_NAME(cls) -> str:
        value = 'classes.json'
        cls.logger.debug(value)
        return value

    @property
    def LAM_PROPERTIES_CONFIG_NAME(cls) -> str:
        value = 'properties.json'
        cls.logger.debug(value)
        return value

    @property
    def LAM_DEFAULT_TIMEOUT(cls) -> str:
        value = int(os.environ.get('LAM_GUNICORN_TIMEOUT', 300))
        cls.logger.debug(value)
        return value

    @property
    def LAM_DOCUMENT_PROPERTY_GRAPH(cls) -> str:
        value = os.environ.get("LAM_DOCUMENT_PROPERTY_GRAPH",
                               "http://publications.europa.eu/resources/authority/lam/DocumentProperty")
        cls.logger.debug(value)
        return value

    @property
    def LAM_CLASSES_GRAPH(cls) -> str:
        value = os.environ.get("LAM_CLASSES_GRAPH",
                               "http://publications.europa.eu/resources/authority/lam/LAMLegalDocument")
        cls.logger.debug(value)
        return value

    @property
    def LAM_CELEX_CLASSES_GRAPH(cls) -> str:
        value = os.environ.get("LAM_CELEX_CLASSES_GRAPH",
                               "http://publications.europa.eu/resources/authority/celex/CelexLegalDocument")
        cls.logger.debug(value)
        return value


config = LAMConfig()


class FlaskConfig:
    """
    Base Flask config
    """
    DEBUG = False
    TESTING = False


class ProductionConfig(FlaskConfig):
    """
    Production Flask config
    """


class DevelopmentConfig(FlaskConfig):
    """
    Development Flask config
    """
    DEBUG = True


class TestingConfig(FlaskConfig):
    """
    Testing Flask config
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
