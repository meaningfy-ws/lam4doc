#!/usr/bin/python3

# config.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
Project wide configuration file.
"""

import os

LAM_DEBUG = os.environ.get('LAM_DEBUG', True)
LAM_FLASK_SECRET_KEY = os.environ.get('LAM_FLASK_SECRET_KEY', 'secret key')


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
