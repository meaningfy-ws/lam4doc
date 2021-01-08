#!/usr/bin/python3

# __init__.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
Module for configuring and exposing the ui server using the Flask framework.
"""

from flask import Flask

from lam4doc.config import config

app = Flask(__name__)

app.config['SECRET_KEY'] = config.LAM_FLASK_SECRET_KEY

from . import views
