import logging
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import peppy
import yaml

log_format = "%(levelname)-8s %(asctime)s   %(message)s"
date_format = "%d/%m %H:%M:%S"
logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)


def generate_global_config(bgcflow_dir, global_config):
    """
    Generate a BGCFlow global configuration file from a template.

    Copies the template configuration file to the specified global configuration path.

    Args:
        bgcflow_dir (str or pathlib.PosixPath): The directory where the BGCFlow configuration is located.
        global_config (str or pathlib.PosixPath): The path to the global configuration file to be generated.
    """
    logging.info(f"Generating config file from template at: {global_config}")
    template_config = bgcflow_dir / ".examples/_config_example.yaml"
    assert (
        template_config.is_file()
    ), "Cannot find template file. Are you using BGCFlow version >= 0.4.1?"

    shutil.copy(template_config, global_config)

    # scan for example projects
    def copy_project_example(project_type):
        """
        Scan global config for example projects and (sub projects) and copy them to the config directory.
        """
        with open(global_config, "r") as file:
            config_yaml = yaml.safe_load(file)
        example_projects = [
            Path(p["pep"])
            for p in config_yaml[project_type]
            if "pep" in p.keys() and p["pep"].endswith(".yaml")
        ]

        for example_project in example_projects:
            example_project_dir = (
                bgcflow_dir / ".examples" / example_project.parent.name
            )
            target_dir = bgcflow_dir / "config" / example_project_dir.name
            if str(example_project).startswith(".examples"):
                logging.warning(
                    f"\n - WARNING: You are using BGCFlow version <= 0.7.1. In the global config file (`{global_config}`), please change the location of your `{example_project}` to `config/{example_project.parent.name}/{example_project.name}`."
                )
            shutil.copytree(example_project_dir, target_dir)

    for project_type in ["projects", "bgc_projects"]:
        copy_project_example(project_type)


def bgcflow_init(bgcflow_dir, global_config):
    """
    Initialize BGCFlow configuration and display available projects.

    Initializes BGCFlow configuration based on the provided directory and global configuration path.
    If the global configuration file exists, it lists the available projects.
    If not, generates a global configuration file from the template and provides instructions for a test run.

    Args:
        bgcflow_dir (str or pathlib.PosixPath): The directory where the BGCFlow configuration is located.
        global_config (str or pathlib.PosixPath): The path to the global configuration file.
    """
    # check if global config available
    if global_config.is_file():
        # grab available projects
        logging.debug(f"Found config file at: {global_config}")
        with open(global_config, "r") as file:
            config_yaml = yaml.safe_load(file)
            project_names = [p for p in config_yaml["projects"]]
            list_of_projects = {}
            for p in project_names:
                if "pep" in p.keys():
                    p["name"] = p.pop("pep")
                if p["name"].endswith(".yaml"):
                    pep = peppy.Project(
                        str(bgcflow_dir / p["name"]), sample_table_index="genome_id"
                    )
                    name = pep.name
                    file_path = pep.config["sample_table"]
                else:
                    name = p["name"]
                    file_path = p["samples"]
                list_of_projects[name] = file_path

            print("Available projects:")
            for p in list_of_projects.keys():
                print(f" - {p} : {file_path}")
    else:
        generate_global_config(bgcflow_dir, global_config)

    print("\nDo a test run by: `bgcflow run -n`")


def generate_project(
    bgcflow_dir,
    project_name,
    pep_version="2.1.0",
    use_project_rules=False,
    samples_csv=False,
    prokka_db=False,
    gtdb_tax=False,
    description=False,
):
    """
    Generate a PEP project configuration in BGCFlow.

    This function creates a configuration file for a Project Enhanced Pipelines (PEP)
    project within the BGCFlow framework. It allows you to define various aspects of
    the project, such as its name, version, description, sample data, custom annotations,
    and more.

    Args:
        bgcflow_dir (str or pathlib.PosixPath): The directory where the BGCFlow configuration is located.
        project_name (str): The name of the project.
        pep_version (str, optional): The version of the PEP specification. Defaults to "2.1.0".
        use_project_rules (bool, optional): Flag indicating whether to use project-specific rules. Defaults to False.
        samples_csv (pd.core.frame.DataFrame or str, optional): Sample data in Pandas DataFrame or path to a CSV file. Defaults to False.
        prokka_db (str, optional): Path to a custom Prokka annotation file. Defaults to False.
        gtdb_tax (str, optional): Path to a custom GTDB taxonomy file. Defaults to False.
        description (str, optional): Description for the project. Defaults to False.
    """

    # Ensure bgcflow_dir is a pathlib.PosixPath
    if not isinstance(bgcflow_dir, Path):
        bgcflow_dir = Path(bgcflow_dir)

    # Define paths and template dictionary
    global_config = bgcflow_dir / "config/config.yaml"
    template_dict = {
        "name": project_name,
        "pep_version": pep_version,
        "description": "<TO DO: give a description to your project>",
        "sample_table": "samples.csv",
        "prokka-db": "OPTIONAL: relative path to your `prokka-db.csv`",
        "gtdb-tax": "OPTIONAL: relative path to your `gtdbtk.bac120.summary.tsv`",
    }

    # Update template_dict with project rules if enabled
    if use_project_rules:
        with open(bgcflow_dir / "workflow/rules.yaml", "r") as file:
            available_rules = yaml.safe_load(file)
            available_rules = {rule: "FALSE" for rule in available_rules.keys()}
            template_dict["rules"] = available_rules

    # Create project directory
    project_dir = bgcflow_dir / f"config/{project_name}"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Handle samples_csv input
    if isinstance(samples_csv, pd.core.frame.DataFrame):
        logging.debug("Generating samples file from Pandas DataFrame")
        assert samples_csv.index.name == "genome_id"
        assert (
            samples_csv.columns
            == [
                "source",
                "organism",
                "genus",
                "species",
                "strain",
                "closest_placement_reference",
            ]
        ).all
        samples_csv.to_csv(project_dir / "samples.csv")
    elif isinstance(samples_csv, str):
        logging.debug(f"Copying samples file from {samples_csv}")
        samples_csv = Path(samples_csv)
        assert samples_csv.is_file()
        shutil.copy(samples_csv, project_dir / "samples.csv")

    # Handle prokka_db input
    if isinstance(prokka_db, str):
        logging.debug(f"Copying custom annotation file from {prokka_db}")
        prokka_db = Path(prokka_db)
        assert prokka_db.is_file()
        shutil.copy(prokka_db, project_dir / "prokka-db.csv")
        template_dict["prokka-db"] = "prokka-db.csv"

    # Handle gtdb_tax input
    if isinstance(gtdb_tax, str):
        logging.debug(f"Copying custom taxonomy from {gtdb_tax}")
        gtdb_tax = Path(gtdb_tax)
        assert gtdb_tax.is_file()
        shutil.copy(gtdb_tax, project_dir / "gtdbtk.bac120.summary.tsv")
        template_dict["gtdb-tax"] = "gtdbtk.bac120.summary.tsv"

    # Update template_dict with project description
    if isinstance(description, str):
        logging.debug("Writing project description...")
        template_dict["description"] = description

    # Generate project configuration file
    logging.info(f"Project config file generated in: {project_dir}")
    with open(project_dir / "project_config.yaml", "w") as file:
        yaml.dump(template_dict, file, sort_keys=False)

    # Initialize global config if not present
    if not global_config.is_file():
        bgcflow_init(bgcflow_dir, global_config)

    # Update global config.yaml with project information
    with open(bgcflow_dir / "config/config.yaml", "r") as file:
        logging.debug("Updating global config.yaml")
        main_config = yaml.safe_load(file)

        # Rename 'pep' to 'name' for consistency
        for item in main_config["projects"]:
            if "pep" in item:
                item["name"] = item.pop("pep")

        # Rename 'pipelines' to 'rules'
        if "pipelines" in main_config.keys():
            main_config["rules"] = main_config.pop("pipelines")

        project_names = [p["name"] for p in main_config["projects"]]
        assert (
            project_name not in project_names
        ), f"Project name: '{project_name}' already exists!\nUse a different name or edit the files in: {project_dir}"
        assert (
            str(project_dir / "project_config.yaml") not in project_names
        ), f"Project name: '{project_name}' already exists!\nUse a different name or edit the files in: {project_dir}"
        main_config["projects"].append(
            {"name": str(project_dir / "project_config.yaml")}
        )

    # Update and save global config
    with open(bgcflow_dir / "config/config.yaml", "w") as file:
        yaml.dump(main_config, file, sort_keys=False)


def projects_util(**kwargs):
    """
    Utility function for managing BGCflow projects.

    Args:
        **kwargs (dict): Keyword arguments for the function.

    Keyword Arguments:
        bgcflow_dir (str): Path to the BGCflow directory.
        project (str): Name of the BGCflow project to generate.
        use_project_pipeline (bool): Whether to use the project-specific pipeline rules.
        prokka_db (str): Path to the Prokka database.
        gtdb_tax (str): Path to the GTDB taxonomy file.
        samples_csv (str): Path to the samples CSV file.
    """

    # pep_version = "2.1.0"
    bgcflow_dir = Path(kwargs["bgcflow_dir"]).resolve()
    config_dir = bgcflow_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    global_config = config_dir / "config.yaml"

    if type(kwargs["project"]) == str:
        # project_name = kwargs["project"]

        generate_project(
            bgcflow_dir,
            kwargs["project"],
            use_project_rules=kwargs["use_project_pipeline"],
            prokka_db=kwargs["prokka_db"],
            gtdb_tax=kwargs["gtdb_tax"],
            samples_csv=kwargs["samples_csv"],
        )
    else:
        bgcflow_init(bgcflow_dir, global_config)


def copy_final_output(**kwargs):
    """
    Copy final project output files to a specified destination.

    This function facilitates the copying of processed project output files to a designated destination. It can
    also preserve symbolic links during the copy process if specified.

    Args:
        **kwargs (dict): Keyword argument for the function.

    Keyword arguments:
        bgcflow_dir (str): The directory where the BGCFlow configuration is located.
        project (str): The name of the project whose output should be copied.
        resolve_symlinks (str, optional): Indicate whether to preserve symbolic links. Defaults to False.
        destination (str): The destination directory where the output should be copied.
    """
    bgcflow_dir = Path(kwargs["bgcflow_dir"]).resolve()
    project_output = bgcflow_dir / f"data/processed/{kwargs['project']}"
    assert (
        project_output.is_dir()
    ), f"ERROR: Cannot find project [{kwargs['project']}] results. Run `bgcflow init` to find available projects."
    if "resolve_symlinks" in kwargs.keys():
        assert kwargs["resolve_symlinks"] in [
            "True",
            "False",
        ], f'Invalid argument {kwargs["resolve_symlinks"]} in --resolve-symlinks. Choose between "True" or "False"'
        if kwargs["resolve_symlinks"] == "True":
            resolve_symlinks = "-L"
    else:
        resolve_symlinks = ""
    exclude_copy = f"{str(project_output.stem)}/bigscape/*/cache"
    command = [
        "rsync",
        "-avPhr",
        resolve_symlinks,
        "--exclude",
        exclude_copy,
        str(project_output),
        kwargs["destination"],
    ]
    logging.debug(f'Running command: {" ".join(command)}')
    subprocess.call(command)
