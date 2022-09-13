"""Console script for bgcflow_wrapper."""
import sys
import click
import bgcflow_wrapper
from snakedeploy.deploy import deploy as dplyr
from git import Repo
from pathlib import Path

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def greeter(**kwargs):
    output = '{0}, {1}!'.format(kwargs['greeting'],
                                kwargs['name'])
    if kwargs['caps']:
        output = output.upper()
    print(output)

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


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=bgcflow_wrapper.__version__)
def main():
    """
    A snakemake wrapper and utility tools for BGCFlow
    """
    pass

@main.command()
@click.argument('destination')
@click.option('--branch', default='main', help='BGCFlow branch/release to use')
def deploy(**kwargs):
    """
    [EXPERIMENTAL] Deploy BGCFlow locally using snakedeploy.

    DESTINATION: path to deploy BGCFlow
    """
    deployer(**kwargs)

@main.command()
@click.argument('destination')
def clone(**kwargs):
    """
    Use git to clone BGCFlow to local directory.

    DESTINATION: path to clone BGCFlow
    """
    cloner(**kwargs)

@main.command()
@click.argument('destination')
@click.argument('name')
def init(**kwargs):
    """
    [COMING SOON] Initiate an empty BGCFlow PEP config file.

    DESTINATION: path BGCFlow directory\n
    NAME: project name
    """
    config_dir = Path(kwargs['destination']) / 'config'
    click.echo(f"Creating PEP file: {kwargs['name']}/project_config.yaml in {config_dir.resolve()}")
    click.echo("Work in progress...")

@main.command()
@click.option('--bgcflow_dir', default='.', help='Location of BGCFlow directory')
def run(**kwargs):
    """
    [COMING SOON] A snakemake wrapper to run BGCFlow.

    """
    click.echo("Work in progress...")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
