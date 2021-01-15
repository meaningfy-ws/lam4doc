# conftest.py
# Date:  2020.11.27
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

# coding=utf-8
"""Functional test cases for LAM - steps implementation"""
import logging
from time import sleep

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

logger = logging.getLogger(__name__)


@scenario('../features/functional_test_cases.feature', 'TC.01 – Access LAM online tool')
def test_tc01__access_lam_online_tool():
    """TC.01 – Access LAM online tool."""


@scenario('../features/functional_test_cases.feature', 'TC.03 – TOC for Properties - Expands and collapses')
def test_tc03_toc_for_properties_expands_and_collapses():
    """TC.03 – TOC for Properties - Expands and collapses"""


@scenario('../features/functional_test_cases.feature', 'TC.03 – TOC for Properties - Selected entry is highlighted')
def test_tc03_toc_for_properties_selected_entry_is_highlighted():
    """TC.03 – TOC for Properties - Selected entry is highlighted"""


@scenario('../features/functional_test_cases.feature', 'TC.04 – TOC for Templates - Expands and collapses')
def test_tc04_toc_for_templates_expands_and_collapses():
    """Pipelines storage not failing."""


@scenario('../features/functional_test_cases.feature', 'TC.05 – TOC for Celex numbers - Expands and collapses')
def test_tc05_toc_for_celex_numbers_expands_and_collapses():
    """Pipelines storage not failing."""


@scenario('../features/functional_test_cases.feature', 'TC.05 – TOC for Celex numbers - Selected entry is highlighted')
def test_tc05_toc_for_celex_numbers_selected_entry_is_highlighted():
    """Pipelines storage not failing."""


@scenario('../features/functional_test_cases.feature', 'Verify that specific properties exist')
def test_verify_that_specific_properties_exist():
    """Pipelines storage not failing."""


@scenario('../features/functional_test_cases.feature', 'Verify that specific classes exist')
def test_verify_that_specific_classes_exist():
    """Pipelines storage not failing."""


@scenario('../features/functional_test_cases.feature', 'Verify that specific CELEXs exist')
def test_verify_that_specific_celexs_exist():
    """Pipelines storage not failing."""


# ------------------------------------------------------------------------------------------------


@given(parsers.cfparse('the baseURI {baseUri:String}', extra_types=dict(String=str)))
def the_baseuri_lam_uri(browser, scenario_context, baseUri):
    """the baseURI LAM_URI."""
    if baseUri == "LAM_URL":
        from tests.config import LAM_URL
        scenario_context["baseURI"] = LAM_URL


@when(parsers.cfparse('I navigate to the location {pageLocation:String}', extra_types=dict(String=str)))
def i_navigate_to_the_location_page(scenario_context, browser, pageLocation):
    browser.get(scenario_context["baseURI"] + pageLocation)


@then(parsers.cfparse('the resulting page contains {content:String} in the element with id {field_id:String}',
                      extra_types=dict(String=str)))
def the_result_page_contains(browser, scenario_context, content, field_id):
    pass


@then(parsers.cfparse('the page has the title {title:String}',
                      extra_types=dict(String=str)))
def the_result_page_contains(browser, scenario_context, title):
    page_title = browser.title
    assert page_title == title


@then(parsers.cfparse('the resulting page contains {content:String} in the element with XPath {xpath:String}',
                      extra_types=dict(String=str)))
def the_result_page_contains(browser, scenario_context, content, xpath):
    element = browser.find_element_by_xpath(xpath)
    assert element.text == content


@then(parsers.cfparse('the resulting page does not contain the element with XPath {xpath:String}',
                      extra_types=dict(String=str)))
def the_result_page_contains(browser, scenario_context, xpath):
    assert browser.find_element_by_xpath(xpath).text == ''


@then(parsers.cfparse('the field with id {field_id:String} is visible', extra_types=dict(String=str)))
def step_impl(browser, scenario_context, field_id):
    assert browser.find_element_by_id(field_id).is_displayed() is True


@then(parsers.cfparse('the field with id {field_id:String} is not visible', extra_types=dict(String=str)))
def step_impl(browser, scenario_context, field_id):
    assert browser.find_element_by_id(field_id).is_displayed() is True


@then(parsers.cfparse('the field with XPath {field_xpath:String} is not visible', extra_types=dict(String=str)))
def step_impl(browser, scenario_context, field_xpath):
    sleep(1)
    assert browser.find_element_by_xpath(field_xpath).is_displayed() is False


@then(parsers.cfparse('the field with XPath {field_xpath:String} is visible', extra_types=dict(String=str)))
def step_impl(browser, scenario_context, field_xpath):
    sleep(1)
    assert browser.find_element_by_xpath(field_xpath).is_displayed() is True


@then(parsers.cfparse('the element with XPath {field_xpath:String} is in the viewport', extra_types=dict(String=str)))
def step_impl(browser, scenario_context, field_xpath):
    sleep(1)
    element = browser.find_element_by_xpath(field_xpath)
    assert is_element_visible_in_viewpoint(browser, element) is True


@then(parsers.cfparse('the field with id {field_id:String} has CSS class {css_class:String}',
                      extra_types=dict(String=str)))
def step_impl(browser, scenario_context, field_id, css_class):
    assert browser.find_element_by_id(field_id).is_displayed() is True


@then(parsers.cfparse('the field with XPath {field_xpath:String} has CSS class {css_class:String}',
                      extra_types=dict(String=str)))
def step_impl(browser, scenario_context, field_xpath, css_class):
    assert str(browser.find_element_by_xpath(field_xpath).get_attribute("class")) == css_class


@when(parsers.cfparse('I click on the button with id {control_id:String}', extra_types=dict(String=str)))
def i_click_on_the_button_with_id_validate_button_id(browser, scenario_context, control_id):
    button = browser.find_element_by_id(control_id)
    button.click()


@then(parsers.cfparse('I switch to the iframe with ID {iframe_id:String}', extra_types=dict(String=str)))
def i_switch_to_the_frame_with_id(browser, scenario_context, iframe_id):
    iframe = browser.find_element_by_id(iframe_id)
    browser.switch_to_frame(iframe)


@when(parsers.cfparse('I switch to the iframe with ID {iframe_id:String}', extra_types=dict(String=str)))
def i_switch_to_the_frame_with_id(browser, scenario_context, iframe_id):
    iframe = browser.find_element_by_id(iframe_id)
    browser.switch_to_frame(iframe)


@when(parsers.cfparse('I click on the element with XPath {xpath:String}', extra_types=dict(String=str)))
def i_click_on_the_element_with_x_path(browser, scenario_context, xpath):
    sleep(1)
    button = browser.find_element_by_xpath(xpath)
    button.click()


@when(parsers.cfparse('I click on the element with ID {element_id:String}', extra_types=dict(String=str)))
def i_click_on_the_element_with_x_path(browser, scenario_context, element_id):
    element = browser.find_element_by_xpath(element_id)
    element.click()


@when(parsers.cfparse('I fill in the field {control_id:String} with {text_value:String}',
                      extra_types=dict(String=str)))
def i_fill_in_the_field_field_id_sparql_with_someendpointhere(scenario_context, browser, control_id, text_value):
    browser.find_element_by_id(control_id).send_keys(scenario_context[text_value])


def is_element_visible_in_viewpoint(driver, element) -> bool:
    return driver.execute_script("var elem = arguments[0],                 "
                                 "  box = elem.getBoundingClientRect(),    "
                                 "  cx = box.left + box.width / 2,         "
                                 "  cy = box.top + box.height / 2,         "
                                 "  e = document.elementFromPoint(cx, cy); "
                                 "for (; e; e = e.parentElement) {         "
                                 "  if (e === elem)                        "
                                 "    return true;                         "
                                 "}                                        "
                                 "return false;                            "
                                 , element)
