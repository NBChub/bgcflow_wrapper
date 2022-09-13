===============
bgcflow_wrapper
===============


.. image:: https://img.shields.io/pypi/v/bgcflow_wrapper.svg
        :target: https://pypi.python.org/pypi/bgcflow_wrapper

.. image:: https://img.shields.io/travis/matinnuhamunada/bgcflow_wrapper.svg
        :target: https://travis-ci.com/matinnuhamunada/bgcflow_wrapper

.. image:: https://readthedocs.org/projects/bgcflow-wrapper/badge/?version=latest
        :target: https://bgcflow-wrapper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A snakemake and snakedeploy wrapper for BGCFlow.


* Free software: MIT license
* Documentation: https://bgcflow-wrapper.readthedocs.io.


Usage:
Clone this repository.
.. highlight:: bash

::
    git clone git@github.com:matinnuhamunada/bgcflow_wrapper.git

Use conda/mamba to create environment and install the package.

::
    cd bgcflow_wrapper
    mamba env create -f env.yaml


Features
--------

::
    Usage: bgcflow_wrapper [OPTIONS] COMMAND [ARGS]...

      A snakemake wrapper and utility tools for BGCFlow

    Options:
      --version   Show the version and exit.
      -h, --help  Show this message and exit.

    Commands:
      clone   Use git to clone BGCFlow to local directory.
      deploy  [EXPERIMENTAL] Deploy BGCFlow locally using snakedeploy.
      init    [COMING SOON] Initiate an empty BGCFlow PEP config file.
      run     [COMING SOON] A snakemake wrapper to run BGCFlow.

.. highlight:: none

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
