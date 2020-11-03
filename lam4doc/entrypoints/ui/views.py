#!/usr/bin/python3

# views.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
UI pages
"""
from flask import render_template

from lam4doc.entrypoints.ui import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='LAM index page')
