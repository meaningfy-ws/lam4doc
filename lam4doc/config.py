#!/usr/bin/python3

# config.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
Project wide configuration file.
"""

import os
from pathlib import Path

LAM_DEBUG = os.environ.get('LAM_DEBUG', True)
LAM_FLASK_SECRET_KEY = os.environ.get('LAM_FLASK_SECRET_KEY', 'secret key')

LAM_API_LOCATION = os.environ.get('LAM_API_LOCATION', 'http://lam-api')
LAM_API_PORT = os.environ.get('LAM_API_PORT', 4050)
LAM_API_SERVICE = f'{LAM_API_LOCATION}:{LAM_API_PORT}'

LAM_FUSEKI_LOCATION = os.environ.get('LAM_FUSEKI_LOCATION', 'http://fuseki')
LAM_FUSEKI_PORT = os.environ.get('LAM_FUSEKI_PORT', 3030)
LAM_FUSEKI_QUERY_URL = os.environ.get('LAM_FUSEKI_QUERY_URL', '/lam/query')
LAM_FUSEKI_SERVICE = f'{LAM_FUSEKI_LOCATION}:{LAM_FUSEKI_PORT}{LAM_FUSEKI_QUERY_URL}'

LAM_REPORT_TEMPLATE_LOCATION = str(Path(__file__).parents[1] / 'templates/content')

LAM_DEFAULT_TIMEOUT = int(os.environ.get('LAM_GUNICORN_TIMEOUT', 300))


LAM_LOGGER = 'lam'


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
