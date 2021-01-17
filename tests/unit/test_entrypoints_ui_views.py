#!/usr/bin/python3

# test_entrypoints_ui_views.py
# Date:  24/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
from bs4 import BeautifulSoup


def _helper_get_request_and_parse(client, url) -> BeautifulSoup:
    response = client.get(url, follow_redirects=True)
    return BeautifulSoup(response.data, 'html.parser')


def test_index(ui_client):
    ui_url = '/'
    soup = _helper_get_request_and_parse(ui_client, ui_url)

    title = soup.find(id='title')
    assert 'LAM index page' in title.get_text()

    report_button = soup.find(id='LAM-report')
    assert 'Generate LAM Report' in report_button.get_text()
    indexes_button = soup.find(id='LAM-indexes')
    assert 'Generate LAM Indexes' in indexes_button.get_text()
