# linkedpipes.feature
# Date:  2020.11.27
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com


Feature: Test basic functionality LAM

    Background:
    Given the baseURI LAM_URL

  Scenario: TC.01 – Access LAM online tool
    When I navigate to the location /celex.html
    Then the page has the title Home - Publications Office of the EU
#    And the field with id "TOC_PART_1" is visible
#    And the field with id "TOC_PART_2" is visible
#    And the field with id "TOC_PART_3" is visible
#    And the field with id "TOC_EXPANDED" is visible
#    And the field with id "SEARCH_BOX" is visible
#    And the field with id "EXTERNAL_LINKS_SECTION" is visible
#    And the field with id "LATEST_NEWS" is visible
#    And the field with id "FEEDBACK" is visible
#    And the field with id "HEADER" is visible
#    And the field with id "FOOTER" is visible
#    And the field with id "NAVIGATION" is visible


    Scenario: TC.02 – Access LAM online tool – automatized/ad-hoc update


    Scenario: TC.03 – TOC for Properties - Expanded by default
    When I navigate to the location /properties.html
    Then the resulting page contains TOC_FOR_PROPERTIES in the element with XPath /some/xpath/here
    And the field with id "TOC_PART_1" has CSS class SOME_CSS_CLASS_HERE


    Scenario: TC.03 – TOC for Properties - Expands and collapses
    When I navigate to the location /location/here
    And I click on the element with ID SOME_TOC_ID_HERE
    Then the field with id "PROPERTY_COLLAPSED_ELEMENT_1" is not visible


    Scenario: TC.03 – TOC for Properties - Selected entry is highlighted
    When I navigate to the location /properties.html
    And I click on the element with XPath /html/body/main/div[2]/ul[2]/li/a
    And I click on the element with ID SOME_TOC_ID_HERE
    Then the field with id "PROPERTY_SELECTED_ELEMENT_1" has CSS class SELECTED_CSS_PROPERTY


    Scenario: TC.04 – TOC for Templates - Expanded by default
    When I navigate to the location /location/here
    Then the resulting page contains TOC_FOR_TEMPLATES in the element with XPath /some/xpath/here
    And the field with id "TOC_PART_1" has CSS class SOME_CSS_CLASS_HERE


    Scenario: TC.04 – TOC for Templates - Expands and collapses
    When I navigate to the location /location/here
    And I click on the element with ID TOC_FOR_TEMPLATES
    Then the field with id "TEMPLATE_COLLAPSED_ELEMENT_1" is not visible


    Scenario: TC.04 – TOC for Templates - Selected entry is highlighted
    When I navigate to the location /location/here
    And I click on the element with ID SOME_TOC_ID_HERE
    Then the field with id "CLASS_SELECTED_ELEMENT_1" has CSS class SELECTED_CSS_CLASS


    Scenario: TC.05 – TOC for Celex numbers - Expanded by default
    When I navigate to the location /location/here
    Then the resulting page contains TOC_FOR_CELEX in the element with XPath /some/xpath/here
    And the field with id "TOC_PART_1" has CSS class SOME_CSS_CLASS_HERE


    Scenario: TC.05 – TOC for Celex numbers - Expands and collapses
    When I navigate to the location /location/here
    And I click on the element with ID TOC_FOR_CELEX
    Then the field with id "CELEX_COLLAPSED_ELEMENT_1" is not visible


    Scenario: TC.05 – TOC for Celex numbers - Selected entry is highlighted
    When I navigate to the location /location/here
    And I click on the element with ID SOME_TOC_ID_HERE
    Then the field with id "CELEX_SELECTED_ELEMENT_1" has CSS class SELECTED_CSS_CELEX

      
    Scenario: TC.13 – Access Templates by using TOC, Consult page for Templates
    When I navigate to the location /location/here
    And I click on the element with ID DRAFT_REGULATION_IN_TOC_FOR_TEMPLATES_lamd:c_001
    Then the field with id The current position is indicated in relevant TOC and in page navigation is visible





#    Scenario: Verify that specific properties exist
#    When I navigate to the location /location/here
#    And I click on the element with ID DRAFT_REGULATION_IN_TOC_FOR_TEMPLATES_lamd:c_001
#    Then the field with id The current position is indicated in relevant TOC and in page navigation is visible
#
#    Scenario: Verify that specific classes exist
#    When I navigate to the location /location/here
#    And I click on the element with ID DRAFT_REGULATION_IN_TOC_FOR_TEMPLATES_lamd:c_001
#    Then the field with id The current position is indicated in relevant TOC and in page navigation is visible
#
#    Scenario: Verify that specific CELEXs exist
#    When I navigate to the location /location/here
#    And I click on the element with ID DRAFT_REGULATION_IN_TOC_FOR_TEMPLATES_lamd:c_001
#    Then the field with id The current position is indicated in relevant TOC and in page navigation is visible


