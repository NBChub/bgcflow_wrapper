## Using as a command line interface
--------
This is the main intention of BGCFlow wrapper usage.

### Overview

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

### Typical Usage
- The first step of using BGCFlow wrapper is to get a copy (or clone) of the main BGCFlow Snakemake workflow.
```bash
# get a clone of BGCFlow in your local machine
bgcflow clone MY_BGCFLOW_PATH #change PATH accordingly
```

- Then, initiate a project config by:
```bash
# initiate an example config and projects from template
bgcflow init --bgcflow_dir MY_BGCFLOW_PATH
```
>This will generate a file called `config.yaml` in the `config/` folder inside the cloned BGCFlow directory

- Once the config files are set, we can do a snakemake dry-run:
```bash
# do a dry-run
bgcflow run -n --bgcflow_dir MY_BGCFLOW_PATH
```
>While the workflow is running, the command automatically serve [`Panoptes-UI`](https://github.com/panoptes-organization/panoptes) at [`localhost:5000`](http://localhost:5000/)` to monitor jobs.

- To find out all the rules that can be added in the configuration file, do:
```bash
# find out available rules
bgcflow pipelines --bgcflow_dir MY_BGCFLOW_PATH
```

- To get more details about each individual rules, do:
```bash
# get description of a rule
bgcflow pipelines --describe antismash --bgcflow_dir MY_BGCFLOW_PATH/
```

- To find out how to cite each rules, do:
```bash
# get citation of a rule
bgcflow pipelines --cite antismash --bgcflow_dir MY_BGCFLOW_PATH/
```
## Using as a python library
--------
You can also generate new projects via python or Jupyter notebooks:
```python
from bgcflow.projects_util import generate_project
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
