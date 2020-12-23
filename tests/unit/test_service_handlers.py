#!/usr/bin/python3

# test_service_handlers.py
# Date:  18/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
from pathlib import Path

from lam4doc import config
from lam4doc.services.handlers import generate_report, prepare_template
from tests.conftest import FakeReportBuilder


def test_prepare_report_template(tmpdir, monkeypatch):
    temp_folder = tmpdir.mkdir('report')
    prepare_template(temp_folder, config.LAM_REPORT_TEMPLATE_LOCATION)

    assert Path.is_file(Path(temp_folder) / 'config.json')
    assert Path.is_dir(Path(temp_folder) / 'templates')


def test_generate_lam_report(tmpdir):
    temp_folder = tmpdir.mkdir('report')
    report_builder = FakeReportBuilder(temp_folder)

    report_path = generate_report(temp_folder, report_builder)

    assert Path(temp_folder) / 'output/main.html' == report_path
    assert report_builder.actions[0] == ('MAKE DOCUMENT', str(temp_folder))
