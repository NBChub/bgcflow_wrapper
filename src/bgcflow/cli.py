"""Console script for bgcflow."""
import subprocess
import sys
from pathlib import Path

import click
import yaml

import bgcflow
from bgcflow.bgcflow import cloner, deployer, get_all_rules, snakemake_wrapper
from bgcflow.metabase import upload_and_sync_to_metabase
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
    "-d",
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory.)",
)
@click.option(
    "--workflow",
    default="workflow/Snakefile",
    help="Select which snakefile to run. Available subworkflows: {BGC | Database | Report | Metabase | lsagbc | ppanggolin}. (DEFAULT: workflow/Snakefile)",
)
@click.option(
    "--monitor-off",
    default=False,
    is_flag=True,
    help="Turn off Panoptes monitoring workflow. (DEFAULT: False)",
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
    "--unlock", is_flag=True, help="Remove a lock on the snakemake working directory."
)
@click.option(
    "--until",
    default=None,
    help="Runs the pipeline until it reaches the specified rules or files.",
)
@click.option(
    "--profile",
    default=None,
    help="Path to a directory containing snakemake profile.",
)
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
    Create projects or initiate BGCFlow config from template. Use --project to create a new BGCFlow project.

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
@click.option(
    "--destination",
    default="results",
    help="Provide a destination path here to copy the results. (DEFAULT: results)",
)
@click.option(
    "--bgcflow_dir",
    default=".",
    help="Location of BGCFlow directory. (DEFAULT: Current working directory)",
)
@click.option(
    "--resolve-symlinks",
    default="True",
    help="Resolve symlinks as actual files/folders when copying. Set this to False if you want to keep them as symlinks. (DEFAULT: True)",
)
def get_result(**kwargs):
    """
    View a tree of a project results or get a copy using Rsync.

    PROJECT: project name
    """
    project_dir = Path(kwargs["bgcflow_dir"]) / f"data/processed/{kwargs['project']}"

    if not project_dir.exists():
        print(f"The project directory {project_dir} does not exist.")
        return

    if kwargs["destination"] is None:
        print(f"Available items from {project_dir}:")
        [print(" -", item.name) for item in project_dir.glob("*")]
        print(
            "Use --destination <DESTINATION> to copy these items to a destination path."
        )
    else:
        print(f"Copying items from {project_dir} to {kwargs['destination']}...")
        copy_final_output(**kwargs)
        print("Copy completed.")


@main.command()
@click.option("--port_markdown", default=8001, help="Port to use. (DEFAULT: 8001)")
# @click.option("--port_metabase", default=3000, help="Port to use. (DEFAULT: 8001)")
@click.option("--port_panoptes", default=5000, help="Port to use. (DEFAULT: 8001)")
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
@click.option(
    "--panoptes",
    is_flag=True,
    help="Run Panoptes server to monitor workflow at http://localhost:5000",
)
@click.option("--project", help="Name of the project. (DEFAULT: all)")
def serve(**kwargs):
    """
    Serve static HTML report or other utilities (Metabase, etc.).
    """
    workflow_dir = Path(kwargs["bgcflow_dir"]) / "workflow"

    # METABASE
    if kwargs["metabase"]:
        subprocess.call(
            f"(cd {workflow_dir.parent.resolve()} && snakemake --snakefile workflow/Metabase -c 1)",
            shell=True,
        )

    # PANOPTES
    if kwargs["panoptes"]:
        subprocess.call(
            f"(cd {workflow_dir.parent.resolve()} && panoptes --port {kwargs['port_panoptes']})",
            shell=True,
        )
    # PROJECT DEFAULT
    elif kwargs["project"] is None:
        click.echo(" - Use bgcflow serve --metabase to start a metabase server.")
        click.echo(
            "\n - Use bgcflow serve --project <PROJECT_NAME> to serve a specific project report."
        )
        bgcflow_dir = Path(kwargs["bgcflow_dir"])
        global_config = bgcflow_dir / "config/config.yaml"
        if global_config.is_file():
            # grab available projects
            with open(global_config, "r") as file:
                config_yaml = yaml.safe_load(file)
                project_names = [p for p in config_yaml["projects"]]
                available_projects = []
                for p in project_names:
                    if "pep" in p.keys():
                        p["name"] = p.pop("pep")
                    if p["name"].endswith(".yaml") or p["name"].endswith(".yml"):
                        with open(bgcflow_dir / p["name"], "r") as pep_file:
                            pep_yaml = yaml.safe_load(pep_file)
                            available_projects.append(pep_yaml["name"])
            if available_projects == []:
                click.echo(" - No projects found.")
            else:
                click.echo(" - Available projects:")
                for project_name in available_projects:
                    click.echo(f"    - {project_name}")
        else:
            click.echo(
                "    - Unable to find global config file. Use --bgcflow_dir to set the right location."
            )
        click.echo("\n - Use bgcflow serve -h, --help for more information.")

    # PROJECT SNAKEMAKE_REPORT
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

    # PROJECT MKDOCS_REPORT
    else:
        bgcflow_dir = kwargs["bgcflow_dir"]
        project_name = kwargs["project"]

        # Define a list of disallowed project names
        disallowed_projects = ["metabase"]

        # Check if the project name is not in the list of disallowed project names
        assert (
            project_name not in disallowed_projects
        ), f"ERROR: Project name '{project_name}' is not allowed."

        port_id = kwargs["port_markdown"]
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
@click.argument("build_type", type=click.Choice(["report", "database"]))
@main.command()
def build(build_type, **kwargs):
    """
    Build Markdown report or use dbt to build DuckDB database.

    bgcflow build "report" will generate a Markdown report from the Jupyter notebook.

    bgcflow build "database" will use dbt to build a DuckDB database from the BGCFlow results.
    """
    dryrun = ""
    bgcflow_dir = Path(kwargs["bgcflow_dir"])
    if kwargs["dryrun"]:
        dryrun = "--dryrun"

    if build_type == "report":
        snakefile = "workflow/Report"
    elif build_type == "database":
        snakefile = "workflow/Database"

    subprocess.call(
        f"cd {bgcflow_dir.resolve()} && snakemake --use-conda -c {kwargs['cores']} --snakefile {snakefile} --keep-going {dryrun} --rerun-incomplete",
        shell=True,
    )


@click.argument("project-name", type=str)
@click.option(
    "--bgcflow-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
    help="The root directory of the BGCFlow project.",
)
@click.option(
    "--dbt-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=None,
    help="The directory containing the dbt project to upload. If None, the directory is inferred from the BGCFlow project directory.",
)
@click.option(
    "--metabase-host",
    type=str,
    default="http://localhost:3000",
    help="The URL of the Metabase server.",
)
@click.option(
    "--mb-username",
    type=str,
    default=None,
    help="The Metabase username. If None, the user will be prompted to enter their username.",
)
@click.option(
    "--mb-password",
    type=str,
    default=None,
    help="The Metabase password. If None, the user will be prompted to enter their password.",
    hide_input=True,
)
@click.option(
    "--dbt-schema",
    type=str,
    default="main",
    help="The name of the dbt schema to use.",
)
@click.option(
    "--metabase-database",
    type=str,
    default=None,
    help="The name of the Metabase database to use.",
)
@click.option(
    "--dbt-database",
    type=str,
    default="dbt_bgcflow",
    help="The name of the dbt database to use.",
)
@click.option(
    "--metabase-http",
    is_flag=True,
    default=True,
    help="Use HTTP instead of HTTPS to connect to Metabase.",
)
@click.option(
    "--dbt-excludes",
    multiple=True,
    help="A list of dbt models to exclude from the synchronization.",
)
@main.command()
def sync(project_name, **kwargs):
    """
    Upload and sync DuckDB database to Metabase.
    """
    upload_and_sync_to_metabase(project_name, **kwargs)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
