from pathlib import Path

# https://github.com/cookiecutter/cookiecutter/issues/824
#   our workaround is to include these utility functions in the CCDS package
from ccds.hook_utils.custom_config import write_custom_config
from ccds.hook_utils.dependencies import write_dependencies

#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#
packages = [
    "black",
    "flake8",
    "isort",
    "pip",
    "python-dotenv",
    "pre-commit",
]

# {% if cookiecutter.dataset_storage.s3 %}
packages += ["awscli"]
# {% endif %} #

# {% if cookiecutter.pydata_packages == "basic" %}
packages += [
    "ipython",
    "jupyter",
    "matplotlib",
    "numpy",
    "pandas",
    "scikit-learn",
]
# {% endif %}

# track packages that are not available through conda
pip_only_packages = [
    "awscli",
    "python-dotenv",
]

#
#  POST-GENERATION FUNCTIONS
#
write_dependencies(
    "{{ cookiecutter.dependency_file }}",
    packages,
    pip_only_packages,
    repo_name="{{ cookiecutter.repo_name }}",
    module_name="{{ cookiecutter.module_name }}",
    python_version="{{ cookiecutter.python_version_number }}",
)

write_custom_config("{{ cookiecutter.custom_config }}")

# Remove LICENSE if "No license file"
if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink()

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
pyproject_text = Path("pyproject.toml").read_text()
Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))
