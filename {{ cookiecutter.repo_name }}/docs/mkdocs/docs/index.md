# {{ cookiecutter.project_name }} documentation!
{% if cookiecutter.project_description is not none %}
## Description

{{ cookiecutter.description}}
{% endif %}
## Commands

The Makefile contains the central entry points for common tasks related to this project.
{% if not cookiecutter.dataset_storage.none %}
### Syncing data to cloud storage

{% if cookiecutter.dataset_storage.s3 -%}
* `make sync_data_up` will use `aws s3 sync` to recursively sync files in `data/` up to `s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/`.
* `make sync_data_down` will use `aws s3 sync` to recursively sync files from `s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/` to `data/`.
{% elif cookiecutter.dataset_storage.azure -%}
* `make sync_data_up` will use `az storage blob upload-batch -d` to recursively sync files in `data/` up to `{{ cookiecutter.dataset_storage.azure.container }}/data/`.
* `make sync_data_down` will use `az storage blob upload-batch -d` to recursively sync files from `{{ cookiecutter.dataset_storage.azure.container }}/data/` to `data/`.
{% elif cookiecutter.dataset_storage.gcs -%}
* `make sync_data_up` will use `gsutil rsync` to recursively sync files in `data/` up to `gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/`.
* `make sync_data_down` will use `gsutil rsync` to recursively sync files in `gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/` to `data/`.
{% endif %}
{% endif %}
