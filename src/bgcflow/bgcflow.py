"""Main module."""
import json
import subprocess
import sys
import time
from pathlib import Path

import click
import requests
import yaml
from git import GitCommandError, Repo
from snakedeploy.deploy import deploy as dplyr


def snakemake_wrapper(**kwargs):
    """
    Wrapper function for running Snakemake with BGCFlow.

    Parameters:
    **kwargs (dict): Keyword arguments for Snakemake and BGCFlow.

    Returns:
    None
    """
    p = "Empty process catcher"

    dryrun = ""
    touch = ""
    unlock = ""
    until = ""

    if kwargs["dryrun"]:
        dryrun = "--dryrun"
    if kwargs["touch"]:
        touch = "--touch"
    if kwargs["unlock"]:
        touch = "--unlock"
    if kwargs["until"] is not None:
        until = f"--until {kwargs['until']}"

    # Run Panoptes if not yet run
    port = int(kwargs["wms_monitor"].split(":")[-1])

    try:
        item = requests.get(f"{kwargs['wms_monitor']}/api/service-info")
        status = item.json()["status"]
        assert status == "running"
        click.echo(f"Panoptes already {status} on {kwargs['wms_monitor']}")
    except requests.exceptions.RequestException:  # This is the correct syntax
        click.echo(
            f"Running Panoptes to monitor BGCFlow jobs at {kwargs['wms_monitor']}"
        )
        p = subprocess.Popen(
            ["panoptes", "--port", str(port)], stderr=subprocess.DEVNULL
        )
        click.echo(f"Panoptes job id: {p.pid}")

    # Connect to Panoptes
    click.echo("Connecting to Panoptes...")
    ctr = 1
    for tries in range(10):
        try:
            item = requests.get(f"{kwargs['wms_monitor']}/api/service-info")
            status = item.json()["status"]
            if status == "running":
                click.echo(f"Panoptes status: {status}")
                break
        except requests.exceptions.RequestException:  # This is the correct syntax
            click.echo(f"Retrying to connect: {ctr}x")
            ctr = ctr + 1
            time.sleep(1)
            pass
        else:
            time.sleep(1)

    # Check Snakefile
    valid_workflows = {"Snakefile" : "Main BGCFlow snakefile for genome mining", 
                        "BGC" : "Subworkflow for comparative analysis of BGCs", 
                        "Report" : "Build a report for a BGCFlow run", 
                        "Database" : "Build a database for a BGCFlow run", 
                        "Metabase" : "Run a metabase server"}

    bgcflow_dir = Path(kwargs["bgcflow_dir"])
    if kwargs["workflow"] in ["workflow/Snakefile", "workflow/BGC", "workflow/Report", "workflow/Database", "workflow/Metabase"]:
        snakefile = bgcflow_dir / kwargs["workflow"]
    elif kwargs["workflow"] in ["Snakefile", "BGC", "Report", "Database", "Metabase"]:
        snakefile = bgcflow_dir / f'workflow/{kwargs["workflow"]}'
    else:
        snakefile = bgcflow_dir / kwargs["workflow"]

    assert snakefile.is_file(), f"Snakefile {snakefile} does not exist. Available workflows are:\n" + "\n".join([f" - {k}: {v}" for k, v in valid_workflows.items()])

    # Run Snakemake
    snakemake_command = f"cd {kwargs['bgcflow_dir']} && snakemake --snakefile {snakefile} --use-conda --keep-going --rerun-incomplete --rerun-triggers mtime -c {kwargs['cores']} {dryrun} {touch} {until} {unlock} --wms-monitor {kwargs['wms_monitor']}"
    click.echo(snakemake_command)
    subprocess.call(snakemake_command, shell=True)
    
    # Kill Panoptes
    try:
        if not type(p) == str:
            click.echo(f"Killing panoptes: PID {p.pid}")
            p.kill()
    except UnboundLocalError as e:
        click.echo(e)
    return


def deployer(**kwargs):
    """
    Deploy the BGCFlow repository to a specified destination using Snakedeploy.

    Parameters:
    **kwargs (dict): Keyword arguments for the deployment.

    Returns:
    None
    """
    dplyr(
        "https://github.com/NBChub/bgcflow.git",
        branch=kwargs["branch"],
        name="bgcflow",
        dest_path=Path(kwargs["destination"]),
        tag=kwargs["tag"],
    )
    return


def cloner(**kwargs):
    """
    Clone the BGCFlow repository to a specified destination.

    Parameters:
    **kwargs (dict): Keyword arguments for the cloning.

    Returns:
    None
    """
    destination_dir = Path(kwargs["destination"])
    click.echo(f"Cloning BGCFlow to {destination_dir}...")
    destination_dir.mkdir(parents=True, exist_ok=True)
    try:
        Repo.clone_from(
            "https://github.com/NBChub/bgcflow.git",
            Path(kwargs["destination"]),
            branch=kwargs["branch"],
        )
    except GitCommandError:
        print(
            f"Oops, it seems {kwargs['destination']} already exists and is not an empty directory."
        )
    return


def get_all_rules(**kwargs):
    """
    Print information about available rules in the BGCFlow repository.

    Parameters:
    **kwargs (dict): Keyword arguments for the function.

    Returns:
    None
    """
    path = Path(kwargs["bgcflow_dir"])
    rule_file = path / "workflow/rules.yaml"

    if rule_file.is_file():
        with open(rule_file, "r") as file:
            data = yaml.safe_load(file)
        try:
            if type(kwargs["describe"]) is str:
                rule_name = kwargs["describe"]
                print(f"Description for {rule_name}:")
                print(f" - {data[rule_name]['description']}")

            if type(kwargs["cite"]) is str:
                rule_name = kwargs["cite"]
                print(f"Citations for {rule_name}:")
                [print("-", c) for c in data[rule_name]["references"]]

            if (not type(kwargs["describe"]) is str) and (
                not type(kwargs["cite"]) is str
            ):
                print("Printing available rules:")
                for item in data.keys():
                    print(f" - {item}")

        except KeyError:
            rule_name = [
                r for r in [kwargs["describe"], kwargs["cite"]] if type(r) is str
            ]
            print(
                f"ERROR: Cannot find rule {rule_name} in dictionary. Find available rules with `bgcflow rules`."
            )

    else:
        print(
            "ERROR: Cannot find BGCFlow directory.\nPoint to the right directory using `--bgcflow_dir <destination>` or clone BGCFlow using `bgcflow clone <destination>`."
        )

    return
