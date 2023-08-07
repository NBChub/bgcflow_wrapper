"""Console script for bgcflow."""
import subprocess
import sys
from pathlib import Path

import click

import bgcflow
from bgcflow.bgcflow import cloner, deployer, get_all_rules, snakemake_wrapper
from bgcflow.mkdocs import generate_mkdocs_report
from bgcflow.projects_util import copy_final_output, projects_util

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=bgcflow.__version__, prog_name="bgcflow_wrapper")
def main():
    """
    A snakemake wrapper and utility tools for BGCFlow (https://github.com/NBChub/bgcflow)
    """
    pass


@main.command()
@click.argument("destination")
@click.option("--branch", default="main", help="BGCFlow branch/release to use")
def deploy(**kwargs):
    """
    [EXPERIMENTAL] Deploy BGCFlow locally using snakedeploy.

    DESTINATION: path to deploy BGCFlow
    """
    deployer(**kwargs)


@main.command()
@click.argument("destination")
@click.option(
    "--branch",
    default="main",
    help="BGCFlow branch. (DEFAULT: `main`)",
)
def clone(**kwargs):
    """
    Get a clone of BGCFlow to local directory.

    DESTINATION: path to clone BGCFlow

    BRANCH: BGCFlow branch to clone.
    """
    cloner(**kwargs)


@main.command()
@click.option(
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory.)",
)
@click.option(
    "--snakefile",
    default="workflow/Snakefile",
    help="Location of the Snakefile relative to BGCFlow directory. (DEFAULT: workflow/Snakefile)",
)
@click.option(
    "--wms-monitor",
    default="http://127.0.0.1:5000",
    help="Panoptes address. (DEFAULT: http://127.0.0.1:5000)",
)
@click.option(
    "-c",
    "--cores",
    default=8,
    help="Use at most N CPU cores/jobs in parallel. (DEFAULT: 8)",
)
@click.option("-n", "--dryrun", is_flag=True, help="Test run.")
@click.option(
    "-t",
    "--touch",
    is_flag=True,
    help="Touch output files (mark them up to date without really changing them).",
)
def run(**kwargs):
    """
    A snakemake CLI wrapper to run BGCFlow. Automatically run panoptes.

    """
    snakemake_wrapper(**kwargs)


@main.command()
@click.option(
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory)",
)
@click.option("--describe", help="Get description of a given pipeline.")
@click.option("--cite", help="Get citation of a given pipeline.")
def pipelines(**kwargs):
    """
    Get description of available pipelines from BGCFlow.

    """
    get_all_rules(**kwargs)


@main.command()
@click.option(
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory)",
)
@click.option(
    "--project",
    help="Initiate a new BGCFlow project. Insert project name: `bgcflow init --project <TEXT>`",
)
@click.option(
    "--use_project_pipeline",
    is_flag=True,
    help="Generate pipeline selection template in PEP file instead of using Global pipelines. Use with `--project` option.",
)
@click.option(
    "--prokka_db", help="Path to custom reference file. Use with `--project` option."
)
@click.option(
    "--gtdb_tax", help="Path to custom taxonomy file. Use with `--project` option."
)
@click.option(
    "--samples_csv", help="Path to samples file. Use with `--project` option."
)
def init(**kwargs):
    """
    Create projects or initiate BGCFlow config. Use --project to create a new BGCFlow project.

    Usage:
    bgcflow init --> check current directory for existing config dir. If not found, generate from template.
    bgcflow init --project <TEXT> --> generate a new BGCFlow project in the config directory.

    """
    try:
        projects_util(**kwargs)
    except FileNotFoundError as e:
        click.echo(
            "ERROR: Cannot find BGCFlow directory.\nPoint to the right directory using `--bgcflow_dir <destination>` or clone BGCFlow using `bgcflow clone <destination>`"
        )
        print(e)


@main.command()
@click.argument("project")
@click.option("--copy", help="Destination path to copy results.")
@click.option(
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory)",
)
@click.option("--copy-links", is_flag=True, help="Resolve symlinks as file/folders.)")
def get_result(**kwargs):
    """
    View a tree of a project results or get a copy using Rsync.

    PROJECT: project name
    """
    if kwargs["copy"] is None:
        project_dir = (
            Path(kwargs["bgcflow_dir"]) / f"data/processed/{kwargs['project']}"
        )
        print(f"Available items from {project_dir}:")
        [print(" -", item.name) for item in project_dir.glob("*")]
        print("Use --copy <DESTINATION> for copying items to destination path")
    else:
        copy_final_output(**kwargs)


@main.command()
@click.option("--port", default=8001, help="Port to use. (DEFAULT: 8001)")
@click.option(
    "--file_server",
    default="http://localhost:8002",
    help="Port to use for fileserver. (DEFAULT: http://localhost:8002)",
)
@click.option(
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory)",
)
@click.option(
    "--metabase",
    is_flag=True,
    help="Run Metabase server at http://localhost:3000. Requires Java to be installed. See: https://www.metabase.com/docs/latest/installation-and-operation/java-versions",
)
@click.option("--project", help="Name of the project. (DEFAULT: all)")
def serve(**kwargs):
    """
    Serve static HTML report or other utilities (Metabase, etc.).
    """
    workflow_dir = Path(kwargs["bgcflow_dir"]) / "workflow"
    if kwargs["metabase"]:
        subprocess.call(
            f"(cd {workflow_dir.parent.resolve()} && snakemake --snakefile workflow/Metabase -c 1)",
            shell=True,
        )
    elif kwargs["project"] is None:
        click.echo(
            "Use `bgcflow serve --project <project name>` to generate report for each project.\nTo see Snakemake run summary, use `bgcflow serve --project snakemake_report`."
        )
    elif kwargs["project"] == "snakemake_report":
        output_dir = Path(kwargs["bgcflow_dir"]) / "data"
        assert (
            output_dir.is_dir()
        ), "ERROR: Cannot find BGCFlow directory. Use --bgcflow_dir to set the right location."
        subprocess.call(
            f"(cd {workflow_dir.parent.resolve()} && snakemake --report index.html)",
            shell=True,
        )
        subprocess.call(
            f"(cd {workflow_dir.resolve()} && jupyter nbconvert --execute --to html --output {output_dir.resolve()}/processed/index.html {workflow_dir.resolve()}/notebook/99-entry_point.ipynb --no-input --template classic)",
            shell=True,
        )
        subprocess.call(
            [
                "python",
                "-m",
                "http.server",
                "--directory",
                kwargs["bgcflow_dir"],
                str(kwargs["port"]),
            ]
        )
    else:
        bgcflow_dir = kwargs["bgcflow_dir"]
        project_name = kwargs["project"]
        port_id = kwargs["port"]
        file_server = kwargs["file_server"]
        generate_mkdocs_report(
            bgcflow_dir, project_name, port_id, file_server, ipynb=False
        )


@click.option(
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory.)",
)
@click.option(
    "-c",
    "--cores",
    default=8,
    help="Use at most N CPU cores/jobs in parallel. (DEFAULT: 8)",
)
@click.option("-n", "--dryrun", is_flag=True, help="Test run.")
@main.command()
def build(**kwargs):
    """
    Use DBT to build DuckDB database from BGCFlow results.
    """
    dryrun = ""
    bgcflow_dir = Path(kwargs["bgcflow_dir"])
    if kwargs["dryrun"]:
        dryrun = "--dryrun"

    subprocess.call(
        f"cd {bgcflow_dir.resolve()} && snakemake --use-conda -c {kwargs['cores']} --snakefile workflow/Database --keep-going {dryrun}",
        shell=True,
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
