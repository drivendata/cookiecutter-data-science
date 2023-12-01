function run_tests () {
    python --version
    python -c "print('python runs....')"

    if [[ $(which python) == *"$1"* ]]; then
        echo "found correct python"
    else
        echo "Python env name $1 not in Python path $(which python)"
        exit 99
    fi

}