import json
import subprocess
import sys
from pathlib import Path

import click
import requests
from dbtmetabase.models.interface import DbtInterface, MetabaseInterface


def upload_and_sync_to_metabase(
    project_name: str,
    bgcflow_dir: str,
    dbt_dir: str,
    metabase_host: str,
    mb_username: str,
    mb_password: str,
    dbt_schema: str = "main",
    dbt_database: str = "dbt_bgcflow",
    metabase_http: bool = True,
    metabase_database: str = None,
    dbt_excludes: list = None,
) -> str:
    """
    Uploads a DuckDB database file generated by dbt to Metabase and syncs the dbt models.

    Args:
        project_name (str): The name of the project to upload to Metabase.
        bgcflow_dir (str): The root directory of the BGCFlow project.
        dbt_dir (str): The directory containing the dbt project to upload. If None, the directory is inferred from the BGCFlow project directory.
        metabase_host (str): The URL of the Metabase server.
        mb_username (str): The Metabase username. If None, the user will be prompted to enter their username.
        mb_password (str): The Metabase password. If None, the user will be prompted to enter their password.
        dbt_schema (str): The name of the dbt schema to use.
        dbt_database (str): The name of the dbt database to use.
        metabase_http (bool): Whether to use HTTP instead of HTTPS to connect to Metabase.
        metabase_database (str): The name of the Metabase database to use. If None, the project name is used.

    Returns:
        str: The output of the dbt-metabase command as a string.

    Raises:
        AssertionError: If the dbt_dir or bgcflow_dir do not exist or are not directories.
        subprocess.CalledProcessError: If the dbt-metabase command fails.
    """
    # available dbt models in bgcflow_dbt-duckdb v0.2.1
    dbt_model_dict = {
        "query-bigslice": ["bigfam_hits", "bigfam_network"],
        "bigscape": ["bigscape_cluster", "bigscape_network", "mibig_hits"],
        "checkm": ["checkm"],
        "seqfu": ["seqfu"],
        "antismash": ["genomes"],
    }

    if dbt_excludes is None:
        dbt_excludes = []
    else:
        dbt_excludes = list(dbt_excludes)

    if dbt_dir is None:
        report_dir = Path(bgcflow_dir) / f"data/processed/{project_name}"
        click.echo(f" - Accessing BGCFlow report directory in: {report_dir}")
        with open(report_dir / "metadata/dependency_versions.json", "r") as f:
            dependency_version = json.load(f)
        antismash_version = dependency_version["antismash"]
        click.echo(f" - AntiSMASH version: {antismash_version}")

        project_metadata_json = report_dir / "metadata/project_metadata.json"
        click.echo(f" - Reading project metadata from: {project_metadata_json}")
        with open(project_metadata_json, "r") as f:
            project_metadata = json.load(f)
        used_pipelines = list(project_metadata[project_name]["rule_used"].keys())
        click.echo(f" - Used pipelines: {', '.join(used_pipelines)}")
        for pipeline in dbt_model_dict.keys():
            if pipeline not in used_pipelines:
                dbt_excludes += dbt_model_dict[pipeline]
        click.echo(f" - Excluding models for sync: {', '.join(dbt_excludes)}")
        dbt_dir = report_dir / f"dbt/antiSMASH_{antismash_version}"

    elif isinstance(dbt_dir, str):
        click.echo(f" - Accessing dbt project directory in: {dbt_dir}")
        click.echo(
            f" - Using all models for sync: {', '.join(list(dbt_model_dict.values()))}"
        )
        dbt_dir = Path(dbt_dir)

    # Get Metabase session token
    if mb_username is None:
        mb_username = click.prompt("Enter your Metabase username")
    if mb_password is None:
        mb_password = click.prompt("Enter your Metabase password", hide_input=True)

    response, session_token = upload_dbt_to_metabase(
        project_name, bgcflow_dir, dbt_dir, metabase_host, mb_username, mb_password
    )
    if response == 200:
        if metabase_database is None:
            metabase_database = project_name
        sync_dbt_models_to_metabase(
            dbt_dir,
            dbt_database,
            metabase_host,
            metabase_database,
            mb_username,
            mb_password,
            dbt_schema,
            metabase_http,
            dbt_excludes,
        )


def upload_dbt_to_metabase(
    project_name: str,
    bgcflow_dir: str,
    dbt_dir: str,
    metabase_host: str,
    mb_username: str,
    mb_password: str,
) -> str:
    """
    Uploads a DuckDB database file generated by dbt to Metabase.

    Args:
        project_name (str): The name of the project to upload to Metabase.
        bgcflow_dir (str): The path to the BGCflow directory.
        dbt_dir (str): The path to the dbt directory containing the DuckDB database file.
        metabase_host (str): The URL of the Metabase server.
        mb_username (str): The username to use for authentication with Metabase.
        mb_password (str): The password to use for authentication with Metabase.

    Returns:
        str: The HTTP status code of the request.

    Raises:
        AssertionError: If the DuckDB database file does not exist or is not a regular file.

    """
    duckdb_path = dbt_dir / "dbt_bgcflow.duckdb"
    assert (
        duckdb_path.is_file()
    ), f"Error: {duckdb_path} does not exist or is not a regular file"

    session_response = requests.post(
        f"{metabase_host}/api/session",
        json={"username": mb_username, "password": mb_password},
    )
    session_token = session_response.json()["id"]

    # Check if database already exists
    database_response = requests.get(
        f"{metabase_host}/api/database", headers={"X-Metabase-Session": session_token}
    )
    databases = database_response.json()
    database_id = None
    for k, v in databases.items():
        if k == "data":
            for db in v:
                if db["name"] == project_name:
                    database_id = db["id"]
                    break

    # Prompt user to continue or cancel upload
    if database_id is not None:
        user_input = input(
            f" - WARNING: A database with the name '{project_name}' already exists in Metabase. Do you want to continue with the upload? (y/n) "
        )
        if user_input.lower() != "y":
            click.echo(" - Database upload cancelled by user")
            return

    # Upload or update database in Metabase
    if database_id is None:
        database_response = requests.post(
            f"{metabase_host}/api/database",
            headers={"X-Metabase-Session": session_token},
            json={
                "engine": "duckdb",
                "name": project_name,
                "details": {"database_file": str(duckdb_path.resolve())},
            },
        )
        if database_response.status_code == 200:
            click.echo(f" - Database '{project_name}' uploaded successfully")
        else:
            click.echo(
                f" - Error uploading database '{project_name}': {database_response.text}"
            )

    else:
        database_response = requests.put(
            f"{metabase_host}/api/database/{database_id}",
            headers={"X-Metabase-Session": session_token},
            json={
                "engine": "duckdb",
                "name": project_name,
                "details": {"database_file": str(duckdb_path.resolve())},
            },
        )
        if database_response.status_code == 200:
            click.echo(f" - Database '{project_name}' updated successfully")
        else:
            click.echo(
                f" - Error updating database '{project_name}': {database_response.text}"
            )

    return database_response.status_code, session_token


def sync_dbt_models_to_metabase(
    dbt_dir: str,
    dbt_database: str,
    metabase_host: str,
    metabase_database: str,
    metabase_user: str,
    metabase_password: str,
    dbt_schema: str = "main",
    metabase_http: bool = True,
    dbt_excludes: list = None,
) -> str:
    """
    Synchronizes dbt models to Metabase using the dbt-metabase package.

    Parameters:
    dbt_dir (str): The path to the dbt project directory.
    dbt_database (str): The name of the dbt database to use.
    metabase_host (str): The URL of the Metabase server.
    metabase_user (str): The username of the Metabase account to use.
    metabase_password (str): The password of the Metabase account to use.
    metabase_database (str): The name of the Metabase database to use.
    dbt_schema (str, optional): The name of the dbt schema to use. Defaults to "main".
    metabase_http (bool, optional): Whether to use HTTP instead of HTTPS for the Metabase connection. Defaults to False.

    Returns:
    str: The output of the dbt-metabase command as a string.
    """
    click.echo(" - Synchronizing dbt models schema to Metabase...")
    if metabase_http:
        click.echo(" - Connecting with HTTP method...")
        metabase_http = "--metabase_http"
    else:
        click.echo(" - Connecting with HTTPS method...")
        metabase_http = "--metabase_https"
    command = [
        "dbt-metabase",
        "models",
        "--dbt_path",
        str(dbt_dir),
        "--dbt_database",
        dbt_database,
        "--metabase_host",
        metabase_host.split("://")[-1],
        "--metabase_user",
        metabase_user,
        "--metabase_password",
        metabase_password,
        "--metabase_database",
        metabase_database,
        "--dbt_schema",
        dbt_schema,
        metabase_http,
    ]
    if dbt_excludes and len(dbt_excludes) > 0:
        command += ["--dbt_excludes", *dbt_excludes]

    # Run the command and capture the output
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )

    #  the output
    click.echo(result.stdout)
    click.echo(result.stderr)
