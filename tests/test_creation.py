import json
import os
import sys
from pathlib import Path
from subprocess import PIPE, run

from conftest import bake_project

BASH_EXECUTABLE = os.getenv("BASH_EXECUTABLE", "bash")


def no_curlies(filepath):
    """Utility to make sure no curly braces appear in a file.
    That is, was Jinja able to render everything?
    """
    data = filepath.open("r").read()

    template_strings = ["{{", "}}", "{%", "%}"]

    template_strings_in_file = [s in data for s in template_strings]
    return not any(template_strings_in_file)


def test_baking_configs(config, fast):
    """For every generated config in the config_generator, run all
    of the tests.
    """
    print("using config", json.dumps(config, indent=2))
    with bake_project(config) as project_directory:
        verify_folders(project_directory, config)
        verify_files(project_directory, config)

        if fast < 2:
            verify_makefile_commands(project_directory, config)


def verify_folders(root, config):
    """Tests that expected folders and only expected folders exist."""
    expected_dirs = [
        ".",
        "data",
        "data/external",
        "data/interim",
        "data/processed",
        "data/raw",
        "docs",
        "models",
        "notebooks",
        "references",
        "reports",
        "reports/figures",
        config["module_name"],
    ]

    if config["include_code_scaffold"] == "Yes":
        expected_dirs += [
            f"{config['module_name']}/data",
            f"{config['module_name']}/features",
            f"{config['module_name']}/models",
            f"{config['module_name']}/visualization",
        ]

    if config["docs"] == "mkdocs":
        expected_dirs += ["docs/docs"]

    expected_dirs = [
        #  (root / d).resolve().relative_to(root) for d in expected_dirs
        Path(d)
        for d in expected_dirs
    ]

    existing_dirs = [
        d.resolve().relative_to(root) for d in root.glob("**") if d.is_dir()
    ]

    assert sorted(existing_dirs) == sorted(expected_dirs)


def verify_files(root, config):
    """Test that expected files and only expected files exist."""
    expected_files = [
        "Makefile",
        "README.md",
        "pyproject.toml",
        "setup.cfg",
        ".env",
        ".gitignore",
        "data/external/.gitkeep",
        "data/interim/.gitkeep",
        "data/processed/.gitkeep",
        "data/raw/.gitkeep",
        "docs/.gitkeep",
        "notebooks/.gitkeep",
        "references/.gitkeep",
        "reports/.gitkeep",
        "reports/figures/.gitkeep",
        "models/.gitkeep",
        f"{config['module_name']}/__init__.py",
    ]

    # conditional files
    if not config["open_source_license"].startswith("No license"):
        expected_files.append("LICENSE")

    if config["include_code_scaffold"] == "Yes":
        expected_files += [
            f"{config['module_name']}/data/__init__.py",
            f"{config['module_name']}/data/make_dataset.py",
            f"{config['module_name']}/features/__init__.py",
            f"{config['module_name']}/features/build_features.py",
            f"{config['module_name']}/models/__init__.py",
            f"{config['module_name']}/models/train_model.py",
            f"{config['module_name']}/models/predict_model.py",
            f"{config['module_name']}/visualization/__init__.py",
            f"{config['module_name']}/visualization/visualize.py",
        ]

    if config["docs"] == "mkdocs":
        expected_files += [
            "docs/mkdocs.yml",
            "docs/README.md",
            "docs/docs/index.md",
            "docs/docs/getting-started.md",
        ]

    expected_files.append(config["dependency_file"])

    expected_files = [Path(f) for f in expected_files]

    existing_files = [f.relative_to(root) for f in root.glob("**/*") if f.is_file()]

    assert sorted(existing_files) == sorted(expected_files)

    for f in existing_files:
        assert no_curlies(root / f)


def verify_makefile_commands(root, config):
    """Actually shell out to bash and run the make commands for:
    - create_environment
    - requirements
    Ensure that these use the proper environment.
    """
    test_path = Path(__file__).parent

    if config["environment_manager"] == "conda":
        harness_path = test_path / "conda_harness.sh"
    elif config["environment_manager"] == "virtualenv":
        harness_path = test_path / "virtualenv_harness.sh"
    elif config["environment_manager"] == "pipenv":
        harness_path = test_path / "pipenv_harness.sh"
    elif config["environment_manager"] == "none":
        return True
    else:
        raise ValueError(
            f"Environment manager '{config['environment_manager']}' not found in test harnesses."
        )

    result = run(
        [BASH_EXECUTABLE, str(harness_path), str(root.resolve())],
        stderr=PIPE,
        stdout=PIPE,
    )
    result_returncode = result.returncode

    encoding = sys.stdout.encoding

    if encoding is None:
        encoding = "utf-8"

    # normally hidden by pytest except in failure we want this displayed
    print("PATH=", os.getenv("PATH"))
    print("\n======================= STDOUT ======================")
    print(result.stdout.decode(encoding))

    print("\n======================= STDERR ======================")
    print(result.stderr.decode(encoding))

    assert result_returncode == 0
