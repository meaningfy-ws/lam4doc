#!/usr/bin/python3

# conftest.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import pytest

from lam4doc.config import TestingConfig
from lam4doc.entrypoints.api import app as api_app


@pytest.fixture
def api_client():
    api_app.config.from_object(TestingConfig())
    return api_app.test_client()
