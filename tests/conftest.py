#!/usr/bin/python3

# conftest.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import pytest

from lam4doc.config import TestingConfig
from lam4doc.entrypoints.api import app as api_app
from lam4doc.entrypoints.ui import app as ui_app


@pytest.fixture
def api_client():
    api_app.config.from_object(TestingConfig())
    return api_app.test_client()


@pytest.fixture
def ui_client():
    ui_app.config.from_object(TestingConfig())
    return ui_app.test_client()


class FakeReportBuilder:
    def __init__(self, target_path, template_name):
        self.target_path = str(target_path)
        self.template = template_name
        self.actions = list()

    def make_document(self):
        self.actions.append(('MAKE DOCUMENT', self.target_path))
