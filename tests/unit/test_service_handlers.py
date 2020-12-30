#!/usr/bin/python3

# test_service_handlers.py
# Date:  18/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
from pathlib import Path

from lam4doc.services.handlers import generate_report
from tests.conftest import FakeReportBuilder


def test_generate_report(tmpdir):
    temp_folder = tmpdir.mkdir('report')
    report_builder = FakeReportBuilder(temp_folder, 'main.html')

    report_path = generate_report(temp_folder, report_builder)

    assert Path(temp_folder) / 'main.html' == report_path
    assert report_builder.actions[0] == ('MAKE DOCUMENT', str(temp_folder))
