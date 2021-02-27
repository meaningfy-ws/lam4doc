# conftest.py
# Date:  2020.11.27
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

import os

LAM_URL = os.environ.get('LAM_URL', 'http://srv.meaningfy.ws:9090')
RUN_HEADLESS_UI_TESTS = os.environ.get('RUN_HEADLESS_UI_TESTS', True)
