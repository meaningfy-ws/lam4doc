#!/usr/bin/python3

# test_service_handlers.py
# Date:  18/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
from pathlib import Path

import pytest

from lam4doc.config import HTML_REPORT_TYPE, PDF_REPORT_TYPE
from lam4doc.services.handlers import generate_report, get_report_location, ReportTypeError
from tests.conftest import FakeReportBuilder


def test_generate_report(tmpdir):
    temp_folder = tmpdir.mkdir('report')
    report_builder = FakeReportBuilder(temp_folder, 'main.html')

    report_path = generate_report(temp_folder, report_builder)

    assert Path(temp_folder) / 'main.html' == report_path
    assert report_builder.actions[0] == ('MAKE DOCUMENT', str(temp_folder))


def test_get_report_location_html():
    report_location = get_report_location(HTML_REPORT_TYPE)
    expected_location = 'templates/html'
    assert report_location[-len(expected_location):] == expected_location


def test_get_report_location_pdf():
    report_location = get_report_location(PDF_REPORT_TYPE)
    expected_location = 'templates/html'
    assert report_location[-len(expected_location):] == expected_location


def test_get_report_location_failure():
    with pytest.raises(ReportTypeError) as e:
        _ = get_report_location('mp3')
    assert 'No acceptable report template location found' in str(e)
