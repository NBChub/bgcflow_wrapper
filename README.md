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


A snakemake wrapper and utility tools for [BGCFlow](https://github.com/NBChub/bgcflow), a systematic workflow for the analysis of biosynthetic gene clusters across large genomic datasets.

For more details, see [documentation](https://NBChub.github.io/bgcflow_wrapper/).

## Publication
> Matin Nuhamunada, Omkar S. Mohite, Patrick V. Phaneuf, Bernhard O. Palsson, and Tilmann Weber. (2023). BGCFlow: Systematic pangenome workflow for the analysis of biosynthetic gene clusters across large genomic datasets. bioRxiv 2023.06.14.545018; doi: [https://doi.org/10.1101/2023.06.14.545018](https://doi.org/10.1101/2023.06.14.545018)

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

## Features
![function](https://raw.githubusercontent.com/NBChub/bgcflow_wrapper/main/docs/assets/Figure_01.png)
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
  build       Build Markdown report or use dbt to build DuckDB database.
  clone       Get a clone of BGCFlow to local directory.
  deploy      [EXPERIMENTAL] Deploy BGCFlow locally using snakedeploy.
  get-result  View a tree of a project results or get a copy using Rsync.
  init        Create projects or initiate BGCFlow config from template.
  pipelines   Get description of available pipelines from BGCFlow.
  run         A snakemake CLI wrapper to run BGCFlow.
  serve       Serve static HTML report or other utilities (Metabase, etc.).
  sync        Upload and sync DuckDB database to Metabase.
```

## Credits

This package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).
