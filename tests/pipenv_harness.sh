#!/bin/bash
set -ex

PROJECT_NAME=$(basename $1)
CCDS_ROOT=$(dirname $0)
MODULE_NAME=$2

# configure exit / teardown behavior
function finish {
    if [[ $(which python) == *"$PROJECT_NAME"* ]]; then
        exit
    fi
    
    pipenv --rm
}
trap finish EXIT

# source the steps in the test
source $CCDS_ROOT/test_functions.sh

# navigate to the generated project and run make commands 
cd $1
make
make create_environment

# can happen outside of environment since pipenv knows based on Pipfile
make requirements

# linting + formatting must happen inside environment
pipenv run make lint
pipenv run make format

# test with pipenv run
pipenv run python -c "import sys; assert \"$PROJECT_NAME\" in sys.executable"

# test importable
pipenv run python -c "import $MODULE_NAME"

# test config importable if scaffolded
if [ -f "$MODULE_NAME/config.py" ]; then
    pipenv run python -c "from $MODULE_NAME import config"
fi
