# LAM 4 DOC
Initiative for Modeling the Legal Analysis Methodology (LAM): Document generation service

# Work in progress

*Currently the project is under heavy development.*

The development version of the LAM HTML content is available [here](http://dev.meaningfy.ws:9090).


### Makefile targets

**install**
- Upgrades PIP to the latest version and installs the local requirements

**test**
- Runs pytest which in turns executes the unit and BDD tests

**build-services**
- Uses docker-compose to build all the services defined in the docker/docker-compose.yml file.

**start-services**
- Uses docker-compose to start the services defined in the docker/docker-compose.yml file.

**stop-services**
- Uses docker-compose to stop the services defined in the docker/docker-compose.yml file.

**generate-indexes**
- Uses [eds4jinja2] to generate the indexes that will later be sent to ElasticSearch for indexing.

**generate-content**
- Uses [eds4jinja2] to generate the content that will be integrated in the portal.

**generate-tests-from-features**
- Based on the feature files, this target generates the missing Python test code.

# Indexes description

## CELEX

A CELEX index record contains the following fields:

- **celexURI**: The URI of the CELEX (for example http://publications.europa.eu/resources/authority/celex/c_1_nnn )
- **rdfTypes**: The RDF type(s) ( for example http://www.w3.org/2004/02/skos/core#Concept )
- **broaderConcepts**: The generalization(s) (for example**: http://publications.europa.eu/resources/authority/celex/c_1 )
- **broaderLabels**: The labels of the associated broader concepts (for example "Treaties")
- **collectionURIS**: The URIs of the collection(s) that the current result belongs to (for example http://publications.europa.eu/resources/authority/celex/class_1 )
- **collectionLabels**: The label(s) of the aforementioned collection(s) (for example "Celex sector 1") 
- **dttValues**: This one or two letters code refers to a specific type of document as indicated in the CELEX number. 
- **dtsValues**: This refers to a specific sector (collection) of documents as indicated in the CELEX number (it is the first number in the celex number).
- **dtaValues**: The year attributed to the document (internal number or ppf number).
- **dtnValues**: A sequential number representing the original reference number of the act. In some instances composed or non-standardised numbers are attributed (e.g. treaties).
- **labels**: The label of the current record, if any.
- **examples**: The example of the current record, if any.
- **editorialNotes**: The editorial note of the current record, if any.

## Classes index

A class index record contains the following fields:

- **classURI**: The URI of the class (for example http://publications.europa.eu/resources/authority/lam/c_108)
- **types**: The RDF type(s) ( for example http://www.w3.org/2004/02/skos/core#Concept )
- **authors**: The author(s) of the current class (for example http://publications.europa.eu/resource/authority/corporate-body/CONSIL)
- **resourceTypes**: The resource type (for example http://publications.europa.eu/resource/authority/resource-type/STRATEGY_COMMON). This is also known as the type of act (lamd:md_fm).
- **collections**: The collection that the current class is part of (for example http://publications.europa.eu/resources/authority/lam/class_3OTHER)
- **dnClassValues**:
- **dc**: The Eurovoc concept for this specific class.
- **ct**: The subject matter concept for this specific class.
- **cc**: The directory code for this specific class.
- **labels**: The label(s) of the current class (for example "Common strategy , Common strategy , Common strategy , Common strategy (CFSP number), Common strategy (CFSP number), Common strategy (CFSP number)")
- **notes**: The notes of the current class (for example "Proposal**: strategy_council.")
- **examples**: The examples for the current class (for example "32003E0897, Common Strategy 2003/897/CFSP of the European Council of 12 December 2003 amending Common Strategy 1999/877/CFSP on Ukraine in order to extend the period of its application , Stratégie commune 2003/897/PESC du Conseil européen du 12 décembre 2003 modifiant la stratégie commune 1999/877/PESC à l'égard de l'Ukraine afin de proroger sa période d'application, 32003E0897, Common Strategy 2003/897/CFSP of the European Council of 12 December 2003 amending Common Strategy 1999/877/CFSP on Ukraine in order to extend the period of its application , Stratégie commune 2003/897/PESC du Conseil européen du 12 décembre 2003 modifiant la stratégie commune 1999/877/PESC à l'égard de l'Ukraine afin de proroger sa période d'application")

For additional information, please consult [this file](./templates/indexes/queries/classes.rq)

## Properties index

A property index record contains the following fields:

- **propertyURI**: The URI of the property (for example http://publications.europa.eu/resources/authority/lam/md_SUSPEND_PAR)
- **types**: The URI of the type of the property (for example http://www.w3.org/2004/02/skos/core#Concept) 
- **propertyCollections**: The URI(s) of the collection(s) that the property is part of (for example http://publications.europa.eu/resources/authority/lam/class_MSEA)
- **propertyCollectionLabels**: The label(s) of the collections that the property is part of (for example "Amendment to/Earlier related instruments")
- **propertyTypes**: The type(s) of the property (for example "object property")
- **skosDefinitions**: The SKOS definition(s) of the property (for example "Partial suspension (SP) - similar as Suspension")
- **editorialNotes**: The editorial notes for the property (for example "08/11/2019: Diferences between suspension and partial suspension? Is this really needed?")
- **examples**: The examples for the property (for example "<j.0:resource_legal_term-of-office rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">VII (2020-2025)</j.0:resource_legal_term-of-office>")
- **historyNotes**: The history notes for the property (for example "Used by EUR-Lex quick search. Relevant for search in internal numbers for ECB, therefore this property is created in some ECB documents on purpose.")
- **scopeNotes**: The scope notes for the property (for example "32013R0298 → 32004R0314")
- **notations**: The notations for the property (for example "SUSPEND_PAR") 
- **labels**: The labels for the property (for example "Link: Partially suspends document")

# Contributing
You are more than welcome to help expand and mature this project. We adhere to [Apache code of conduct](https://www.apache.org/foundation/policies/conduct), please follow it in all your interactions on the project.   

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the maintainers of this repository before making a change.

## Licence 
This project is licensed under [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) licence. 

Powered by [Meaningfy](https://github.com/meaningfy-ws).


[eds4jinja2]: <https://pypi.org/project/eds4jinja2/> "eds4jinja2 on pypi"