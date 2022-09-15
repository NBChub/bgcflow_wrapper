# bgcflow_wrapper
[![Snakemake](https://img.shields.io/badge/snakemake-≥7.14.0-brightgreen.svg)](https://snakemake.bitbucket.io)

A snakemake wrapper and utility tools for [BGCFlow](https://github.com/NBChub/bgcflow).

## Usage
--------
Clone this repository:

    git clone git@github.com:matinnuhamunada/bgcflow_wrapper.git

Use conda/mamba to create environment and install the package:

    cd bgcflow_wrapper
    mamba env create -f env.yaml
    cd ..

>**Developer Note**: BGCFlow wrapper are still in development phase. We will make it available to install using `pip` when BGCFlow wrapper is released.

## Features
--------
```bash

$ bgcflow_wrapper

Usage: bgcflow_wrapper [OPTIONS] COMMAND [ARGS]...

  A snakemake wrapper and utility tools for BGCFlow
  (https://github.com/NBChub/bgcflow)

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  clone   Use git to clone BGCFlow to local directory.
  deploy  [EXPERIMENTAL] Deploy BGCFlow locally using snakedeploy.
  init    Create projects or initiate BGCFlow config files from template.
  rules   Get description of available rules from BGCFlow.
  run     A snakemake CLI wrapper to run BGCFlow.
```

## Tutorial
--------
```bash
# get a clone of BGCFlow in your local machine
bgcflow_wrapper clone MY_BGCFLOW_PATH #change PATH accordingly

# initiate an example config and projects from template
bgcflow_wrapper init --bgcflow_dir MY_BGCFLOW_PATH

# do a dry-run
bgcflow_wrapper run -n --bgcflow_dir MY_BGCFLOW_PATH
```

## Generating BGCFlow projects from Jupyter Notebooks
--------
You can also generate new projects from Jupyter notebooks:
```python
from bgcflow_wrapper.projects_util import generate_project
import pandas as pd

df_samples = pd.read_csv('samples.csv', index_col=0)
description = "Project generated from notebook"

generate_project("BGCFLOW_PATH",
                "MY_PROJECT",
                use_project_rules=True,
                samples_csv=df_samples,
                prokka_db="prokka-db.csv",
                gtdb_tax="gtdbtk.bac120.summary.tsv",
                description=description
                )
```

## Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.
