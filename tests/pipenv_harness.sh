#!/bin/bash
set -ex

PROJECT_NAME=$(basename $1)
CCDS_ROOT=$(dirname $0)

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
make create_environment

# can happen outside of environment since pipenv knows based on Pipfile
make requirements

# test with pipenv run
pipenv run python -c "import sys; assert \"$PROJECT_NAME\" in sys.executable"
