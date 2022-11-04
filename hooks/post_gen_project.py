# https://github.com/cookiecutter/cookiecutter/issues/824
#   our workaround is to include these utility functions in the CCDS package
from urllib.request import urlretrieve

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
    "setuptools",
    "wheel",
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

# {% if cookiecutter.nbautoexport == "yes" %}
packages += ["nbautoexport"]
pip_only_packages += ["nbautoexport"]
# {% endif %}

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

# {% if cookiecutter.ethics_checklist == "yes" %}
urlretrieve(
    "https://raw.githubusercontent.com/drivendataorg/deon/master/examples/ethics.md",
    "ethics.md",
)
# {% endif %}
