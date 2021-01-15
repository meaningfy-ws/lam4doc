# functional_test_cases.feature
# Date:  2020.11.27
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com


Feature: Test basic functionality LAM

    Background:
    Given the baseURI LAM_URL

  Scenario: TC.01 – Access LAM online tool
    When I navigate to the location /
    Then the page has the title Home - Publications Office of the EU
    And I switch to the iframe with ID content
    And the field with XPath //li[@data-unique='document-properties'] is visible
    And the field with XPath //li[@data-unique='lam-classes'] is visible
    And the field with XPath //li[@data-unique='celex-classes'] is visible
    And the field with XPath //li[@data-unique='-references-[cl]-'] is visible


    Scenario: TC.03 – TOC for Properties - Expands and collapses
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='document-properties']
    And I click on the element with XPath //li[@data-unique='celex-classes']
    Then the field with XPath //li[@data-unique='-references-[cl]-'] is not visible


   Scenario: TC.03 – TOC for Properties - Selected entry is highlighted
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='document-properties']
    And I click on the element with XPath //li[@data-unique='-essential-information-[cl]-']
    Then the field with XPath //li[@data-unique='-essential-information-[cl]-'] has CSS class tocify-item ui-widget-content ui-state-hover ui-state-default


    Scenario: TC.04 – TOC for Templates - Expands and collapses
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='lam-classes']
    And I click on the element with XPath //li[@data-unique='-case-law-[cl]-']
    Then the field with XPath //li[@data-unique='-case-law-[cl]-'] is visible
    And the element with XPath //*[@id="http://publications.europa.eu/resources/authority/lam/class_CASE"] is in the viewport
    And the field with XPath //li[@data-unique='celex-classes'] has CSS class tocify-item ui-widget-content
    And the field with XPath //li[@data-unique='document-properties'] has CSS class tocify-item ui-widget-content


    Scenario: TC.05 – TOC for Celex numbers - Expands and collapses
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='celex-classes']
    And I click on the element with XPath //li[@data-unique='-treaty-full-text-[cn]-']
    Then the field with XPath //li[@data-unique='-treaty-full-text-[cn]-'] is visible
    And the element with XPath //*[@id="http://publications.europa.eu/resources/authority/celex/c_1_TXT"] is in the viewport
    And the field with XPath //li[@data-unique='lam-classes'] has CSS class tocify-item ui-widget-content
    And the field with XPath //li[@data-unique='document-properties'] has CSS class tocify-item ui-widget-content


    Scenario: TC.05 – TOC for Celex numbers - Selected entry is highlighted
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='celex-classes']
    And I click on the element with XPath //li[@data-unique='-celex-sector-1-[cl]-']
    And I click on the element with XPath //li[@data-unique='-declaration-annexed-to-the-final-act-[cn]-']
    Then the field with XPath //li[@data-unique='-declaration-annexed-to-the-final-act-[cn]-'] has CSS class tocify-item ui-widget-content ui-state-hover ui-state-default


    Scenario: Verify that specific properties exist
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='document-properties']
    And I click on the element with XPath //li[@data-unique='-references-[cl]-']
    And I click on the element with XPath //li[@data-unique='-celex-number-[cl]-']
    And I click on the element with XPath //li[@data-unique='-celex-sector-[cn]-']
    Then the element with XPath //*[@id="http://publications.europa.eu/resources/authority/lam/md_DTS"] is in the viewport


    Scenario: Verify that specific classes exist
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='lam-classes']
    And I click on the element with XPath //li[@data-unique='-legal-acts-[cl]-']
    And I click on the element with XPath //li[@data-unique='-legislative-acts-[cl]-']
    Then the element with XPath //*[@id="http://publications.europa.eu/resources/authority/lam/class_LEGIS"] is in the viewport


    Scenario: Verify that specific CELEXs exist
    When I navigate to the location /
    And I switch to the iframe with ID content
    And I click on the element with XPath //li[@data-unique='celex-classes']
    And I click on the element with XPath //li[@data-unique='-celex-sector-2-[cl]-']
    And I click on the element with XPath //li[@data-unique='-agreements-with-member-or-non-member-states-or-international-organisations-[cn]-']
    Then the element with XPath //*[@id="http://publications.europa.eu/resources/authority/celex/c_2_A_OJC"] is in the viewport