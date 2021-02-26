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
ZIP_REPORT_TYPE = 'zip'
DEFAULT_REPORT_TYPE = HTML_REPORT_TYPE
REPORT_EXTENSIONS = [HTML_REPORT_TYPE, PDF_REPORT_TYPE]


class LAMConfig:
    logger_name = 'lam'
    logger = logging.getLogger(logger_name)

    @property
    def LAM_LOGGER(self) -> str:
        value = self.logger_name
        self.logger.debug(value)
        return value

    @property
    def LAM_DEBUG(self) -> str:
        value = os.environ.get('LAM_DEBUG', True)
        self.logger.debug(value)
        return value

    @property
    def LAM_FLASK_SECRET_KEY(self) -> str:
        value = os.environ.get('LAM_FLASK_SECRET_KEY', 'secret key')
        self.logger.debug(value)
        return value

    @property
    def LAM_API_SERVICE(self) -> str:
        location = os.environ.get('LAM_API_LOCATION', 'http://lam-api')
        port = os.environ.get('LAM_API_PORT', 4050)
        value = f'{location}:{port}'
        self.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_SERVICE(self) -> str:
        location = os.environ.get('LAM_FUSEKI_LOCATION', 'http://fuseki')
        port = os.environ.get('LAM_FUSEKI_PORT', 3030)
        value = f'{location}:{port}'
        self.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_REPORT_URL(self) -> str:
        location = os.environ.get('LAM_FUSEKI_LOCATION', 'http://fuseki')
        port = os.environ.get('LAM_FUSEKI_PORT', 3030)
        query_url = os.environ.get('LAM_FUSEKI_QUERY_URL', '/lam/query')
        value = f'{location}:{port}{query_url}'
        self.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_USERNAME(self) -> str:
        value = os.environ.get('LAM_FUSEKI_USERNAME', 'admin')
        self.logger.debug(value)
        return value

    @property
    def LAM_FUSEKI_PASSWORD(self) -> str:
        value = os.environ.get('LAM_FUSEKI_PASSWORD', 'admin')
        self.logger.debug(value)
        return value

    @property
    def LAM_HTML_REPORT_TEMPLATE_LOCATION(self) -> str:
        value = str(Path(__file__).parents[1] / 'templates/html')
        self.logger.debug(value)
        return value

    @property
    def LAM_PDF_REPORT_TEMPLATE_LOCATION(self) -> str:
        value = str(Path(__file__).parents[1] / 'templates/pdf')
        self.logger.debug(value)
        return value

    @property
    def LAM_PDF_REPORT_TEMPLATE_LATEX_FILES(self) -> list:
        filenames = ['main-all.tex', 'main-celex-classes.tex', 'main-lam-classes.tex', 'main-lam-properties.tex']
        self.logger.debug(filenames)
        return filenames

    @property
    def LAM_INDEXES_TEMPLATE_LOCATION(self) -> str:
        value = str(Path(__file__).parents[1] / 'templates/indexes')
        self.logger.debug(value)
        return value

    @property
    def LAM_CELEX_CONFIG_NAME(self) -> str:
        value = 'celex.json'
        self.logger.debug(value)
        return value

    @property
    def LAM_CLASSES_CONFIG_NAME(self) -> str:
        value = 'classes.json'
        self.logger.debug(value)
        return value

    @property
    def LAM_PROPERTIES_CONFIG_NAME(self) -> str:
        value = 'properties.json'
        self.logger.debug(value)
        return value

    @property
    def LAM_DEFAULT_TIMEOUT(self) -> str:
        value = int(os.environ.get('LAM_GUNICORN_TIMEOUT', 300))
        self.logger.debug(value)
        return value

    @property
    def LAM_DOCUMENT_PROPERTY_GRAPH(self) -> str:
        value = os.environ.get("LAM_DOCUMENT_PROPERTY_GRAPH",
                               "http://publications.europa.eu/resources/authority/lam/DocumentProperty")
        self.logger.debug(value)
        return value

    @property
    def LAM_CLASSES_GRAPH(self) -> str:
        value = os.environ.get("LAM_CLASSES_GRAPH",
                               "http://publications.europa.eu/resources/authority/lam/LAMLegalDocument")
        self.logger.debug(value)
        return value

    @property
    def LAM_CELEX_CLASSES_GRAPH(self) -> str:
        value = os.environ.get("LAM_CELEX_CLASSES_GRAPH",
                               "http://publications.europa.eu/resources/authority/celex/CelexLegalDocument")
        self.logger.debug(value)
        return value

    @property
    def LAM_INDEXES_ZIP_NAME(self) -> str:
        value = 'indexes.zip'
        self.logger.debug(value)
        return value

    @property
    def LAM_ALL_ZIP_NAME(self) -> str:
        value = 'lam_assets.zip'
        self.logger.debug(value)
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
