# BGCFlow Wrapper


<p align="left">
<a href="https://pypi.python.org/pypi/bgcflow_wrapper">
    <img src="https://img.shields.io/pypi/v/bgcflow_wrapper.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/NBChub/bgcflow_wrapper/actions">
    <img src="https://github.com/NBChub/bgcflow_wrapper/actions/workflows/dev.yml/badge.svg?" alt="CI Status">
</a>

<a href="https://NBChub.github.io/bgcflow_wrapper/">
    <img src="https://img.shields.io/website/https/NBChub.github.io/bgcflow_wrapper/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">
</a>

</p>


A snakemake wrapper and utility tools for [BGCFlow](https://github.com/NBChub/bgcflow).

For more details, see [documentation](https://NBChub.github.io/bgcflow_wrapper/).


## Setup
--------
### Setup via Conda
To install `bgcflow_wrapper` with conda, run this command in your
terminal:

```bash
# create and activate new conda environment
conda create -n bgcflow pip -y
conda activate bgcflow

# install BGCFlow wrapper
pip install git+https://github.com/NBChub/bgcflow_wrapper.git
```

### Setup via Python venv
Alternative, using python virtual environment:
````bash
# create and activate python virtual environment
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
  clone       Get a clone of BGCFlow to local directory.
  deploy      [EXPERIMENTAL] Deploy BGCFlow locally using snakedeploy.
  get-result  View a tree of a project results or get a copy using Rsync.
  init        Create projects or initiate BGCFlow config.
  pipelines   Get description of available pipelines from BGCFlow.
  run         A snakemake CLI wrapper to run BGCFlow.
  serve       Serve static HTML report or other utilities (Metabase, etc.).
```

## Credits

This package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).
