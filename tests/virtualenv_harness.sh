#!/bin/bash
set -e

PROJECT_NAME=$(basename $1)
CCDS_ROOT=$(dirname $0)

# configure exit / teardown behavior
function finish {
    if [[ $(which python) == *"$PROJECT_NAME"* ]]; then
        deactivate
    fi

    if [ ! -z `which rmvirtualenv` ]; then
        rmvirtualenv $PROJECT_NAME
    elif [ ! -z `which rmvirtualenv.bat` ]; then
        rmvirtualenv.bat $PROJECT_NAME
    fi
}
trap finish EXIT

# source the steps in the test
source $CCDS_ROOT/test_functions.sh

# navigate to the generated project and run make commands
cd $1

if [ -z $TMPDIR ]
then
    windowstmpdir=/c/Users/VssAdministrator/AppData/Local/Temp
    if [ -e $windowstmpdir ]
    then
        export TMPDIR=$windowstmpdir
    fi
fi

TEMP_ENV_ROOT=$(mktemp -d "${TMPDIR:-/tmp/}$(basename $0).XXXXXXXXXXXX")
export WORKON_HOME=$TEMP_ENV_ROOT

if [ ! -z `which virtualenvwrapper.sh` ]
then
    source `which virtualenvwrapper.sh`
fi

make create_environment

# workon not sourced

if [ -e $TEMP_ENV_ROOT/$PROJECT_NAME/bin/activate ]
then
    . $TEMP_ENV_ROOT/$PROJECT_NAME/bin/activate
else
    . $TEMP_ENV_ROOT/$PROJECT_NAME/Scripts/activate
fi

make requirements

run_tests $PROJECT_NAME
