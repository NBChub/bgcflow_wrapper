"""Console script for bgcflow_wrapper."""
import sys
import click
import bgcflow_wrapper
from bgcflow_wrapper.bgcflow_wrapper import cloner, deployer, snakemake_wrapper, get_all_rules
from bgcflow_wrapper.projects_util import projects_util


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=bgcflow_wrapper.__version__)
def main():
    """
    A snakemake wrapper and utility tools for BGCFlow (https://github.com/NBChub/bgcflow)
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
@click.option('--bgcflow_dir', default='.', help='Location of BGCFlow directory. (DEFAULT: Current working directory.)')
@click.option('--snakefile', default='workflow/Snakefile', help='Location of the Snakefile relative to BGCFlow directory. (DEFAULT: workflow/Snakefile)')
@click.option('--wms-monitor', default='http://127.0.0.1:5000', help='Panoptes address. (DEFAULT: http://127.0.0.1:5000)')
@click.option('-c', '--cores', default=32, help='Use at most N CPU cores/jobs in parallel. (DEFAULT: 32)')
@click.option('-n', '--dryrun', is_flag=True, help='Test run.')
@click.option('-t', '--touch', is_flag=True, help='Touch output files (mark them up to date without really changing them).')
def run(**kwargs):
    """
    A snakemake CLI wrapper to run BGCFlow. Automatically run panoptes.

    """
    snakemake_wrapper(**kwargs)


@main.command()
@click.option('--bgcflow_dir', default='.', help='Location of BGCFlow directory. (DEFAULT: Current working directory)')
def rules(**kwargs):
    """
    Get description of available rules from BGCFlow.

    """
    click.echo("Printing all BGCFlow rules:")
    get_all_rules(**kwargs)

@main.command()
@click.option('--bgcflow_dir', default='.', help='Location of BGCFlow directory. (DEFAULT: Current working directory)')
@click.option('--project', help='Initiate a new BGCFlow project. Insert project name: `bgcflow_wrapper init --project <TEXT>`')
@click.option('--use_own_rules', is_flag=True, help='Generate rule selection template in PEP file instead of using Global rules. Use with `--project` option.')
@click.option('--prokka_db', help='Path to custom reference file. Use with `--project` option.')
@click.option('--gtdb_tax', help='Path to custom taxonomy file. Use with `--project` option.')
@click.option('--samples_csv', help='Path to samples file. Use with `--project` option.')
def init(**kwargs):
    """
    Initiate BGCFlow config files from template. Use --project to create a new BGCFlow project.

    Usage:
    bgcflow_wrapper init --> check current directory for existing config dir. If not found, generate from template.
    bgcflow_wrapper init --project <TEXT> --> generate a new BGCFlow project in the config directory.

    """
    try:
        projects_util(**kwargs)
    except FileNotFoundError as e:
        click.echo("ERROR: Cannot find BGCFlow directory. Use `--bgcflow_dir` to locate BGCFlow directory or `bgcflow_wrapper clone` to get a local copy.")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
