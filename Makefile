include docker/.env

BUILD_PRINT = \e[1;34mSTEP: \e[0m

#-----------------------------------------------------------------------------
# Basic commands
#-----------------------------------------------------------------------------

install:
	@ echo "$(BUILD_PRINT)Installing the local requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements/dev.txt

test:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ pytest

build-services:
	@ echo -e '$(BUILD_PRINT)Building the containers'
	@ docker-compose --file docker/docker-compose.yml --env-file docker/.env build

start-services:
	@ echo -e '$(BUILD_PRINT)(dev) Starting the containers'
	@ docker-compose --file docker/docker-compose.yml --env-file docker/.env up -d

stop-services:
	@ echo -e '$(BUILD_PRINT)(dev) Stopping the containers'
	@ docker-compose --file docker/docker-compose.yml --env-file docker/.env stop

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

generate-content:
	@ echo -e '$(BUILD_PRINT)Generating the content'
	@ mkreport --target ./templates/content/ --output ./docker/nginx/www/
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