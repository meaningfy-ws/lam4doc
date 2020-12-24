#!/usr/bin/python3

# test_service_handlers.py
# Date:  18/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
from json import dumps, load
from pathlib import Path

from lam4doc.services.handlers import generate_report, setup_config_for_index
from tests.conftest import FakeReportBuilder


def test_setup_config_for_index(tmpdir, monkeypatch):
    config_dict = {
        'template': 'main.html',
        'conf': {
            'default_endpoint': 'http://default.config/url',
            'title': 'LAM Report',
        }
    }
    default_config_file = tmpdir.mkdir('default').join('config.json')
    default_config_file.write(dumps(config_dict))
    config_file = setup_config_for_index(tmpdir, default_config_file)

    assert Path(tmpdir / 'config.json').is_file()
    with config_file.open('r') as config:
        assert load(config)['conf']['default_endpoint'] == 'http://fuseki:3030/lam/query'


def test_generate_report(tmpdir):
    temp_folder = tmpdir.mkdir('report')
    report_builder = FakeReportBuilder(temp_folder, 'main.html')

    report_path = generate_report(temp_folder, report_builder)

    assert Path(temp_folder) / 'main.html' == report_path
    assert report_builder.actions[0] == ('MAKE DOCUMENT', str(temp_folder))
