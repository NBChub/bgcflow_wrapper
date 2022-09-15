"""Main module."""
from pathlib import Path
import subprocess
import requests
import sys
import click
from snakedeploy.deploy import deploy as dplyr
from git import Repo
import json
import time

def snakemake_wrapper(**kwargs):
    bgcflow_dir = Path(kwargs['bgcflow_dir'])
    snakefile_path = bgcflow_dir / kwargs['snakefile']

    p = "Empty process catcher"

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
    click.echo('Connecting to Panoptes...')
    ctr = 1
    for tries in range(10):
        try:
            item = requests.get(f"{kwargs['wms_monitor']}/api/service-info")
            status = item.json()['status']
            if status == 'running':
                click.echo(f"Panoptes status: {status}")
                break
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            click.echo(f"Retrying to connect: {ctr}x")
            ctr = ctr + 1
            time.sleep(1)
            pass
        else:
            time.sleep(1)

    # run snakemake
    snakemake_command = f"cd {kwargs['bgcflow_dir']} && snakemake --use-conda --keep-going --rerun-incomplete --rerun-triggers mtime -c {kwargs['cores']} {dryrun} {touch} --wms-monitor {kwargs['wms_monitor']}"
    click.echo(snakemake_command)
    snakemake_run = subprocess.call(snakemake_command , shell=True)
    try:
        if not type(p) == str:
            click.echo(f"Killing panoptes: PID {p.pid}")
            p.kill()
    except UnboundLocalError as e:
        click.echo(e)
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
    Repo.clone_from("https://github.com/NBChub/bgcflow.git", Path(kwargs['destination']),
                    branch=kwargs['branch'])
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
        print("ERROR: Cannot find BGCFlow directory.\nPoint to the right directory using `--bgcflow_dir <destination>` or clone BGCFlow using `bgcflow_wrapper clone <destination>`.")

    return