import json
import shutil
import sys
import tempfile
from contextlib import contextmanager
from itertools import cycle, product
from pathlib import Path

import pytest

from ccds.__main__ import api_main

CCDS_ROOT = Path(__file__).parents[1].resolve()


default_args = {
    "project_name": "my_test_project",
    "repo_name": "my-test-repo",
    "module_name": "project_module",
    "author_name": "DrivenData",
    "description": "A test project",
}


def config_generator(fast=False):
    cookiecutter_json = json.load((CCDS_ROOT / "ccds.json").open("r"))

    # python versions for the created environment; match the root
    # python version since Pipenv needs to be able to find an executable
    running_py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    py_version = [("python_version_number", v) for v in [running_py_version]]

    configs = product(
        py_version,
        [
            ("environment_manager", opt)
            for opt in cookiecutter_json["environment_manager"]
        ],
        [("dependency_file", opt) for opt in cookiecutter_json["dependency_file"]],
        [("pydata_packages", opt) for opt in cookiecutter_json["pydata_packages"]],
    )

    def _is_valid(config):
        config = dict(config)
        #  Pipfile + pipenv only valid combo for either
        if (config["environment_manager"] == "pipenv") ^ (
            config["dependency_file"] == "Pipfile"
        ):
            return False
        # conda is the only valid env manager for environment.yml
        if (config["dependency_file"] == "environment.yml") and (
            config["environment_manager"] != "conda"
        ):
            return False
        return True

    # remove invalid configs
    configs = [c for c in configs if _is_valid(c)]

    # cycle over all values other multi-select fields that should be inter-operable
    # and that we don't need to handle with combinatorics
    cycle_fields = [
        "dataset_storage",
        "open_source_license",
        "include_code_scaffold",
        "docs",
    ]
    cyclers = {k: cycle(cookiecutter_json[k]) for k in cycle_fields}

    for ind, c in enumerate(configs):
        config = dict(c)
        config.update(default_args)
        # Alternate including the code scaffold
        for field, cycler in cyclers.items():
            config[field] = next(cycler)
        config["repo_name"] += f"-{ind}"
        yield config

        # just do a single config if fast passed once or three times
        if fast == 1 or fast >= 3:
            break


def pytest_addoption(parser):
    """Pass -F/--fast multiple times to speed up tests

    default - execute makefile commands, all configs

     -F - execute makefile commands, single config
     -FF - skip makefile commands, all configs
     -FFF - skip makefile commands, single config
    """
    parser.addoption(
        "--fast",
        "-F",
        action="count",
        default=0,
        help="Speed up tests by skipping configs and/or Makefile validation",
    )


@pytest.fixture
def fast(request):
    return request.config.getoption("--fast")


def pytest_generate_tests(metafunc):
    # setup config fixture to get all of the results from config_generator
    if "config" in metafunc.fixturenames:
        metafunc.parametrize(
            "config", config_generator(metafunc.config.getoption("fast"))
        )


@contextmanager
def bake_project(config):
    temp = Path(tempfile.mkdtemp(suffix="data-project")).resolve()

    api_main.cookiecutter(
        str(CCDS_ROOT),
        no_input=True,
        extra_context=config,
        output_dir=temp,
        overwrite_if_exists=True,
    )

    yield temp / config["repo_name"]

    # cleanup after
    shutil.rmtree(temp)
