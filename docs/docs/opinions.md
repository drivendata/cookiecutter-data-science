# Opinions

There are some opinions implicit in the default structure that have grown out of our experience with what works and what doesn't when collaborating on data science projects. Some of the opinions are about workflows, and some of the opinions are about tools that make life easier. Here are some of the beliefs which this project is built on—if you've got thoughts, please [contribute or share them](#contributing).

## Data analysis is a directed acyclic graph

In a strong evidentiary argument, each claim is supported by one or more claims or axioms further upstream. Similarly, in a valid data analysis project, each intermediate value leading to the final product is either data from an external system of record or is the result of such data passing through a piece of code.

**Every piece of data or work product in an analysis tree should be the result of a dependency graph** that can be **traced backwards** to examine what combination of code and data it came from or **run forwards** to recreate any artifact of the analysis. To put this in terms of data structures, a proper data analysis pipeline is a directed acyclic graph ([DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph)).

### Data is immutable

That proper data analysis is a DAG entails that **data must be treated as immutable**—it's okay to read and copy data to manipulate it into new outputs, but never okay to change it in place. This informs the design of the default `data/` directory subfolders in which data originates from `raw` and `external`, intermediate analytical outputs get serialized or cached in `interim`, and final products end up in `processed` (the number or names of these folders is less important than flow of data between them). 

Some **do**s and **don't**s that follow from treating data analysis as a DAG:

* **Do** write code that moves the raw data through a pipeline to your final analysis.
* **Do** serialize or cache the intermediate outputs of long-running steps.
* **Do** make it possible (and ideally, documented and automated) for anyone to reproduce your final data products with only the code in `{{ cookiecutter.module_name }}` and the data in `data/raw` (and `data/external`).

* **Don't** _ever_ edit your raw data, especially not manually, and _especially_ not in Excel. This includes changing file formats or fixing errors that might break a tool that's trying to read your data file.
* **Don't** overwrite your raw data with a newly processed or cleaned version.
* **Don't** save multiple versions of the raw data. 

### Data should (mostly) not be kept in source control

Another consequence of treating data as immutable is that it doesn't need source control in the same way that code does. Therefore, ***by default, the `data` folder is included in the `.gitignore` file.*** If you have a small amount of data that rarely changes, you _may_ want to include the data in the repository. GitHub [currently](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#file-size-limits) warns you if files are over 50MB and rejects any files over 100MB. Some other options for storing/syncing large data include [AWS S3](https://aws.amazon.com/s3/) with a syncing tool (e.g., [`cloudpathlib`](https://github.com/drivendataorg/cloudpathlib), [`s3cmd`](https://s3tools.org/s3cmd)), [`geesefs`](https://github.com/yandex-cloud/geesefs), [Git Large File Storage](https://git-lfs.github.com/), [Git Annex](https://git-annex.branchable.com/), and [dat](https://github.com/dat-ecosystem/dat).

### Tools for DAGs

DAGs are so common in data and software processes that many tools have been built to manage them. We prefer [`make`](https://www.gnu.org/software/make/) for managing steps that depend on each other, especially the long-running	 ones. Make is a common tool on Unix-based platforms (and is available for Windows via [chocolatey](https://community.chocolatey.org/packages/make)). Following the [`make` documentation](https://www.gnu.org/software/make/), [Makefile conventions](https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html#Makefile-Conventions), and [portability guide](https://www.gnu.org/savannah-checkouts/gnu/autoconf/manual/autoconf-2.69/html_node/Portable-Make.html#Portable-Make) will help ensure your Makefiles work effectively across systems. Here are [some](http://zmjones.com/make/) [examples](https://blog.kaggle.com/2012/10/15/make-for-data-scientists/) to [get started](https://web.archive.org/web/20150206054212/https://www.bioinformaticszen.com/post/decomplected-workflows-makefiles/). A number of data folks use `make` as their tool of choice, including [Mike Bostock](https://bost.ocks.org/mike/make/).

There are other tools for managing DAGs that are written in Python instead of a DSL (e.g., [Luigi](https://luigi.readthedocs.org/en/stable/index.html), [Airflow](https://airflow.apache.org/index.html), [Snakemake](https://snakemake.readthedocs.io/en/stable/), [Ruffus](http://www.ruffus.org.uk/), [Prefect](https://github.com/PrefectHQ/prefect), [Dagster](https://github.com/dagster-io/dagster), and [Joblib](https://joblib.readthedocs.io/en/latest/memory.html)). Feel free to use these if they are more appropriate for your analysis.

## Notebooks are for exploration and communication, source files are for repetition

Notebook packages like [Jupyter notebook](https://jupyter.org/), [Zeppelin](https://zeppelin-project.org/), and other literate programming tools are very effective for exploratory data analysis because they enable rapid iteration and visualization of results. However, these tools can be less effective for reproducing an analysis. Source code is superior for replicability because it is more portable, can be tested more easily, and is easier to code review. 

When we use notebooks in our work, we often subdivide the `notebooks` folder to keep things organized and legible. For example, `notebooks/exploratory` contains initial explorations, whereas `notebooks/reports` is more polished work that can be exported as html to the `reports` directory. We also recommend that you follow a naming convention that shows the owner and the order the analysis was done in. We use the format `<step>-<ghuser>-<description>.ipynb` (e.g., `0.3-bull-visualize-distributions.ipynb`). Since notebooks are challenging objects for source control (e.g., diffs of the `json` are often not human-readable and merging is near impossible), we recommended not collaborating directly with others on Jupyter notebooks. We also recommend using a tool like [`nbautoexport`](https://github.com/drivendataorg/nbautoexport) to make reviewing changes to notebooks more facile. 

### Refactor the good parts into source code 

Don't write code to do the same task in multiple notebooks. If it's a data preprocessing task, put it in the pipeline at `{{ cookiecutter.module_name }}/data/make_dataset.py` and load data from `data/interim`. If it's useful utility code, refactor it to `{{ cookiecutter.module_name }}`. Classic signs that you are ready to move from a notebook to source code include duplicating old notebooks to start new ones, copy/pasting functions between notebooks, and creating object-oriented classes within notebooks.

We make it easy to refactor notebook code because the ccds template makes your project a Python package by default and installs it locally in the requirements file of your chosen environment manager. This enables you to import your project's source code and use it in notebooks with a cell like the following:

```python
# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in {{ cookiecutter.module_name }}, it gets loaded
%autoreload 2

from {{ cookiecutter.module_name }}.data import make_dataset
```

## Keep your modeling organized

Different modeling pipelines are different, so we don't provide a lot of baked-in structure to the `models/` directory. However, documenting modelling experiments is critical to enable reproducibility, continuous learning, and improvement. You should implement experiment documentation procedures that enable you to, at minimum, identify the provenance of the data and the version of the code that the experiment used, as well as the metrics used to measure performance.

For smaller projects, starting with homegrown tracking in standard file formats like `json` is fine. You can graduate to experiment tracking tools (e.g., [MLflow](https://mlflow.org/)) if it's warranted or if they're the lingua franca for your team.


## Build from the environment up

The first step in reproducing an analysis is always replicating the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.


Doing so in Python requires choosing and configuring an environment management tool. The ecosystem for this tooling has evolved a lot in recent years. We tend to prefer [`anaconda`](https://www.anaconda.com/download) for managing environments and dependencies these days, but [`pipenv`](https://pipenv.pypa.io/en/latest/), [`poetry`](https://python-poetry.org/), and our previously recommended [`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/) are all valid choices. Cookiecutter v2 lets you pick from among many of these, or to initialize your project without one so you can roll your own. 

If you have more complex requirements for recreating your environment, consider a virtual machine based approach such as [Docker](https://www.docker.com/) or [Vagrant](https://www.vagrantup.com/). Both of these tools use text-based formats (Dockerfile and Vagrantfile respectively) that you can easily add to source control to describe how to create a virtual machine with the requirements you need. You might also consider using [`pip-tools`](https://github.com/jazzband/pip-tools) or [`conda-lock`](https://github.com/conda/conda-lock) to generate a file that appropriately pins your dependencies.

## Keep secrets and configuration out of version control

You _really_ don't want to leak your AWS secret key or Postgres username and password on Github—see the [Twelve Factor App](https://12factor.net/config) principles on this point. Here's one way to do this:

### Store your secrets and config variables in a special file

Create a `.env` file in the project root folder. Thanks to the `.gitignore`, this file should never get committed into the version control repository. Here's an example:

```nohighlight
# example .env file
DATABASE_URL=postgres://username:password@localhost:5432/dbname
AWS_ACCESS_KEY=myaccesskey
AWS_SECRET_ACCESS_KEY=mysecretkey
OTHER_VARIABLE=something
```

### Use a package to load these variables automatically.

If you look at the stub script in `{{ cookiecutter.module_name }}/data/make_dataset.py`, it uses a package called [python-dotenv](https://github.com/theskumar/python-dotenv) to load up all the entries in this file as environment variables so they are accessible with `os.environ.get`. Here's an example snippet adapted from the `python-dotenv` documentation:

```python
# {{ cookiecutter.module_name }}/data/dotenv_example.py
import os
from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

database_url = os.environ.get("DATABASE_URL")
other_variable = os.environ.get("OTHER_VARIABLE")
```

### AWS CLI configuration

When using Amazon S3 to store data, a simple method of managing AWS access is to set your access keys to environment variables. However, managing mutiple sets of keys on a single machine (e.g. when working on multiple projects) it is best to use a [credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html), typically located in `~/.aws/credentials`. A typical file might look like:
```
[default]
aws_access_key_id=myaccesskey
aws_secret_access_key=mysecretkey

[another_project]
aws_access_key_id=myprojectaccesskey
aws_secret_access_key=myprojectsecretkey
```
You can add the profile name when initialising a project; assuming no applicable environment variables are set, the profile credentials will be used be default.

## Encourage adaptation from a consistent default

To keep this structure broadly applicable for many different kinds of projects, we think the best approach is to be liberal in changing the folders around for _your_ project, but be conservative in modifying the default cookiecutter structure for _all_ projects.

We've created a <span class="label label-info">folder-layout</span> label specifically for issues proposing to add, subtract, rename, or move folders around. More generally, we've also created a <span class="label label-warning">needs-discussion</span> label for issues that should have some careful discussion and broad support before being implemented.

### Examples of template adaptation and evolution

A project's organizational needs may differ from the start and can change over time. Here are a few examples of how we've adapted this template in our own work.

#### Example 1: Simplifying

Some projects don't require multiple sub-directories to organize their module code. When a few python files can effectively accomplish all that is required, flattening folders into files can make things easier to track and maintain. You can see an example of this in our [cyfi package](https://github.com/drivendataorg/cyfi/tree/main/cyfi)). If it's in the template but you don't need it, delete it!

#### Example 2: Expanding

By contrast, we've added more folders to organize module code on more complex projects. A good example of this is our [zamba package](https://github.com/drivendataorg/zamba/tree/master/zamba)) for which we've introduced new folders to handle task-specific portions of the codebase.

#### Example 3: Re-organizing

On long-running projects, the `notebooks` folder can get congested. One adaptation we've employed is to add a top-level `research/` folder (and a corresponding `data/research` data folder) that contains sub-folders for individual experiments. These sub-folders can contain their own notebooks, code, and even their own Makefiles that inherit from the parent project `Makefile`.
