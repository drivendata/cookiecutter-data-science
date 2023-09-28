# Cookiecutter Data Science

_A logical, reasonably standardized but flexible project structure for doing and sharing data science work._

**Cookiecutter Data Science (CCDS)** is a tool for setting up a data science project template that incorporates best practices. To learn more about CCDS's philosophy, visit the project homepage](https://drivendata.github.io/cookiecutter-data-science/).

> ℹ️ Cookiecutter Data Science v2 has changed from v1. It now requires installing the new cookiecutter-data-science Python package, which extends the functionality of the [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) templating utility. Use the provided `ccds` command-line program instead of `cookiecutter`.

## Installation

Cookiecutter Data Science v2 requires Python 3.7+. Since this is a cross-project utility application, we recommend installing it with [pipx](https://pypa.github.io/pipx/). Installation command options:

```bash
# With pipx from PyPI (recommended)
pipx install cookiecutter-data-science

# With pip from PyPI
pip install cookiecutter-data-science

# With conda from conda-forge (coming soon)
# conda install cookiecutter-data-science -c conda-forge
```

## Starting a new project

To start a new project, run:

```bash
ccds https://github.com/drivendata/cookiecutter-data-science
```

[![asciicast](https://asciinema.org/a/244658.svg)](https://asciinema.org/a/244658)

### The resulting directory structure

The directory structure of your new project will look something like this (depending on the settings that you choose):

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for {{ cookiecutter.module_name }}
│                         and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── {{ cookiecutter.module_name }}                <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes {{ cookiecutter.module_name }} a Python module
    │
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── build_features.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
    │   └── train_model.py
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
```

### Initializing a git repo

Create a git repo and push it there:

```bash
git init
git add .
git commit -m "first awesome commit"
git remote add origin <path_to_repo>
git push -u origin main
```

### Pre-commit hooks

This template uses [pre-commit](https://pre-commit.com/) to help ensure that all code is formatted correctly and passes basic checks before you commit it to git. To install pre-commit hooks, run:

```bash
pre-commit install
pre-commit run --all-files
```

## Using v1

If you want to use the old v1 project template, you need to have either the cookiecutter-data-science package or cookiecutter package installed. Then, use either command-line program with the `-c v1` option:

```bash
ccds https://github.com/drivendata/cookiecutter-data-science -c v1
# or equivalently
cookiecutter https://github.com/drivendata/cookiecutter-data-science -c v1
```

## Contributing

We welcome contributions! [See the docs for guidelines](https://drivendata.github.io/cookiecutter-data-science/#contributing).

### Installing development requirements

```bash
pip install -r dev-requirements.txt
```

### Running the tests

```bash
pytest tests
```
