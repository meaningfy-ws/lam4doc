# conftest.py
# Date:  2020.11.27
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


@pytest.fixture(scope="session")
def scenario_context():
    return {}


@pytest.fixture(scope="session")
def browser():
    chrome_options = Options()
    from tests.config import RUN_HEADLESS_UI_TESTS
    if RUN_HEADLESS_UI_TESTS:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_driver_args = ["--whitelisted-ips=", "--log-path=chromedriver.log"]
    _browser = WebDriver(chrome_options=chrome_options, service_args=chrome_driver_args)
    _browser.maximize_window()
    yield _browser
    _browser.close()
    _browser.quit()
