"""Main module."""
from pathlib import Path
import subprocess
import requests
import sys
import click
from snakedeploy.deploy import deploy as dplyr
from git import Repo
import json

def snakemake_wrapper(**kwargs):
    bgcflow_dir = Path(kwargs['bgcflow_dir'])
    snakefile_path = bgcflow_dir / kwargs['snakefile']

    dryrun = ""
    touch = ""

    if kwargs["dryrun"]:
        dryrun = "--dryrun"
    if kwargs["touch"]:
        touch = "--touch"

    # run panoptes if not yet run
    port = int(kwargs['wms_monitor'].split(":")[-1])

    try:
        item = requests.get(f"{kwargs['wms_monitor']}/api/service-info")
        status = item.json()['status']
        assert status == 'running'
        click.echo(f"Panoptes already {status} on {kwargs['wms_monitor']}")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        click.echo(f"Running Panoptes to monitor BGCFlow jobs at {kwargs['wms_monitor']}")
        p = subprocess.Popen(["panoptes", "--port", str(port)], stderr=subprocess.DEVNULL)
        click.echo(f"Panoptes job id: {p.pid}")

    # run snakemake
    snakemake_run = subprocess.call(f"snakemake --use-conda --keep-going --rerun-incomplete \
                                    --rerun-triggers mtime -c {kwargs['cores']} --snakefile \
                                    {snakefile_path} {dryrun} {touch} --wms-monitor \
                                    {kwargs['wms_monitor']}", shell=True)
    try:
        p.kill()
    except UnboundLocalError as e:
        print(e)
    return

def deployer(**kwargs):
    dplyr('https://github.com/NBChub/bgcflow.git',
           branch=kwargs['branch'],
           name="bgcflow",
           dest_path=Path(kwargs['destination']),
           tag="v0.3.3-alpha"
         )
    return

def cloner(**kwargs):
    destination_dir = Path(kwargs['destination'])
    click.echo(f"Cloning BGCFlow to {destination_dir}...")
    destination_dir.mkdir(parents=True, exist_ok=True)
    Repo.clone_from("https://github.com/NBChub/bgcflow.git", Path(kwargs['destination']))
    return

def get_all_rules(**kwargs):

    path = Path(kwargs['bgcflow_dir'])
    rule_file = path / "workflow/rules/rules.json"

    if rule_file.is_file():
        with open(rule_file, "r") as file:
            data = json.load(file)

            for item in data.keys():
                print(f" - {item}")
    else:
        print("ERROR: Cannot find BGCFlow directory.\n       Point to the right directory using `--bgcflow_dir <destination>` or clone BGCFlow using `bgcflow_wrapper clone <destination>`.")

    return