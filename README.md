# BGCFlow Wrapper


<p align="left">
<a href="https://pypi.python.org/pypi/bgcflow_wrapper">
    <img src="https://img.shields.io/pypi/v/bgcflow_wrapper.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/NBChub/bgcflow_wrapper/actions">
    <img src="https://github.com/NBChub/bgcflow_wrapper/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<a href="https://NBChub.github.io/bgcflow_wrapper/">
    <img src="https://img.shields.io/website/https/NBChub.github.io/bgcflow_wrapper/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">
</a>

</p>


A snakemake wrapper and utility tools for [BGCFlow](https://github.com/NBChub/bgcflow).

For more details, see [documentation](https://NBChub.github.io/bgcflow_wrapper/).


## Setup
--------
To install bgcflow_wrapper, run this command in your
terminal:

```bash
# create a new virtual environment
python -m venv env
source env/bin/activate

# install BGCFlow wrapper
pip install git+https://github.com/NBChub/bgcflow_wrapper.git
```

## Features
--------
```bash

$ bgcflow

Usage: bgcflow [OPTIONS] COMMAND [ARGS]...

  A snakemake wrapper and utility tools for BGCFlow
  (https://github.com/NBChub/bgcflow)

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  build       Use DBT to build DuckDB database from BGCFlow results.
  clone       Use git to clone BGCFlow to local directory.
  deploy      [EXPERIMENTAL] Deploy BGCFlow locally using snakedeploy.
  get-result  View a tree of a project results or get a copy using Rsync.
  init        Create projects or initiate BGCFlow config.
  rules       Get description of available rules from BGCFlow.
  run         A snakemake CLI wrapper to run BGCFlow.
  serve       Generate static HTML report for BGCFlow run(s)
```

## Credits

This package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).
