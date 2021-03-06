include docker/.env

BUILD_PRINT = \e[1;34mSTEP: \e[0m

#-----------------------------------------------------------------------------
# Basic commands
#-----------------------------------------------------------------------------

install:
	@ echo "$(BUILD_PRINT)Installing the local requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements/dev.txt
	@ sudo ./requirements/install_chrome_and_driver.sh
	@ sudo apt-get install -y zip texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra texlive-bibtex-extra

test:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ pytest --html=report.html --self-contained-html

test-with-ui:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ (export RUN_HEADLESS_UI_TESTS=False; export LAM_URL=http://srv.meaningfy.ws:9090; pytest -s --html=report.html --self-contained-html)

build-services:
	@ echo -e '$(BUILD_PRINT)Building the containers'
	@ docker-compose --file docker/docker-compose.yml --env-file .env build

start-services:
	@ echo -e '$(BUILD_PRINT)(dev) Starting the containers'
	@ docker-compose --file docker/docker-compose.yml --env-file .env up -d

stop-services:
	@ echo -e '$(BUILD_PRINT)(dev) Stopping the containers'
	@ docker-compose --file docker/docker-compose.yml --env-file .env stop

generate-indexes:
	@ echo -e '$(BUILD_PRINT)(dev) Generating indices for CELEX...'
	@ mkreport --target ./templates/indexes/ --config celex.json --output ./output/celex/
	@ mv ./output/celex/template.json ./docker/nginx/www/celex.json
	@ echo -e '$(BUILD_PRINT)(dev) Generating indices for CLASSES...'
	@ mkreport --target ./templates/indexes/ --config classes.json --output ./output/classes/
	@ mv ./output/classes/template.json ./docker/nginx/www/classes.json
	@ echo -e '$(BUILD_PRINT)(dev) Generating indices for PROPERTIES...'
	@ mkreport --target ./templates/indexes/ --config properties.json --output ./output/properties/
	@ mv ./output/properties/template.json ./docker/nginx/www/properties.json
	@ echo -e '$(BUILD_PRINT)(dev) Cleaning up...'
	@ rm -rf ./output/celex/
	@ rm -rf ./output/classes/
	@ rm -rf ./output/properties/

generate-html:
	@ echo -e '$(BUILD_PRINT)Generating the HTML content'
	@ mkreport --target ./templates/html/ --output ./docker/nginx/www/

generate-pdf:
	@ echo -e '$(BUILD_PRINT)Generating the PDF'

	@ echo -e '$(BUILD_PRINT)(dev) Generating PDF for CELEX...'
	@ cd templates/pdf/; mkreport --config main-celex.json --xelatex
	@ mv ./templates/pdf/output/main-celex-classes.pdf ./docker/nginx/www/main-celex-classes.pdf

# 	@ echo -e '$(BUILD_PRINT)(dev) Generating PDF for Properties...'
# 	@ cd templates/pdf/; mkreport --config main-properties.json --xelatex
# 	@ mv ./templates/pdf/output/main-lam-properties.pdf ./docker/nginx/www/main-lam-properties.pdf
#
# 	@ echo -e '$(BUILD_PRINT)(dev) Generating PDF for LAM Classes...'
# 	@ cd templates/pdf/; mkreport --config main-classes.json --xelatex
# 	@ mv ./templates/pdf/output/main-lam-classes.pdf ./docker/nginx/www/main-lam-classes.pdf
#
# 	@ echo -e '$(BUILD_PRINT)(dev) Generating PDF for the whole LAM content...'
# 	@ cd templates/pdf/; mkreport --config main-all.json --xelatex
# 	@ mv ./templates/pdf/output/main-all.pdf ./docker/nginx/www/main-all.pdf

generate-zip: generate-indexes generate-content generate-pdf
	@ echo -e '$(BUILD_PRINT)Generating the ZIP file'
	@ (cd ./docker/nginx/www/; zip -r everything.zip .)
#-----------------------------------------------------------------------------
# Gherkin feature and acceptance test generation commands
#-----------------------------------------------------------------------------

FEATURES_FOLDER = tests/features
STEPS_FOLDER = tests/steps
FEATURE_FILES := $(wildcard $(FEATURES_FOLDER)/*.feature)
EXISTENT_TEST_FILES = $(wildcard $(STEPS_FOLDER)/*.py)
HYPOTHETICAL_TEST_FILES :=  $(addprefix $(STEPS_FOLDER)/test_, $(notdir $(FEATURE_FILES:.feature=.py)))
TEST_FILES := $(filter-out $(EXISTENT_TEST_FILES),$(HYPOTHETICAL_TEST_FILES))

generate-tests-from-features: $(TEST_FILES)
	@ echo "$(BUILD_PRINT)The following test files should be generated: $(TEST_FILES)"
	@ echo "$(BUILD_PRINT)Done generating missing feature files"
	@ echo "$(BUILD_PRINT)Verifying if there are any missing step implementations"
	@ py.test --generate-missing --feature $(FEATURES_FOLDER)

$(addprefix $(STEPS_FOLDER)/test_, $(notdir $(STEPS_FOLDER)/%.py)): $(FEATURES_FOLDER)/%.feature
	@ echo "$(BUILD_PRINT)Generating the testfile "$@"  from "$<" feature file"
	@ pytest-bdd generate $< > $@
	@ sed -i  's|features|../features|' $@