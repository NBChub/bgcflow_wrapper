# bgcflow_wrapper
[![Snakemake](https://img.shields.io/badge/snakemake-≥7.14.0-brightgreen.svg)](https://snakemake.bitbucket.io)

A snakemake and snakedeploy wrapper for BGCFlow.

## Usage
--------
Clone this repository

    git clone git@github.com:matinnuhamunada/bgcflow_wrapper.git

Use conda/mamba to create environment and install the package::

    cd bgcflow_wrapper
    mamba env create -f env.yaml


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
      init    [COMING SOON] Initiate an empty BGCFlow PEP config file.
      rules   Get description of available rules from BGCFlow.
      run     A snakemake CLI wrapper to run BGCFlow.
```

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.
