from pathlib import Path, PosixPath
import peppy
import yaml, json
import shutil
import pandas as pd
import subprocess

def generate_global_config(bgcflow_dir, global_config):
    """
    Copy config.yaml from template to config directory
    """
    print(f"Generating config file from template at: {global_config}")
    template_config = bgcflow_dir / ".examples/_config_example.yaml"
    assert template_config.is_file(), "Cannot find template file. Are you using BGCFlow version >= 0.4.1?"
    shutil.copy(template_config, global_config)
    return

def bgcflow_init(bgcflow_dir, global_config):
    """
    Initiate a config from template
    """
    # check if global config available
    if global_config.is_file():
        # grab available projects
        print(f"Found config file at: {global_config}")
        with open(global_config, "r") as file:
            config_yaml = yaml.safe_load(file)
            project_names = [p for p in config_yaml['projects']]
            list_of_projects = {}
            for p in project_names:
                print(p)
                if p['name'].endswith('.yaml'):
                    pep = peppy.Project(p['name'], sample_table_index="genome_id")
                    name = pep.name
                    file_path = pep.config['sample_table']
                else:
                    name = p['name']
                    file_path = p['samples']
                list_of_projects[name] = file_path

            print("Available projects:")
            for p in list_of_projects.keys():
                print(f" - {p} : {file_path}")
    else:
        generate_global_config(bgcflow_dir, global_config)
    
    print("Do a test run by: `bgcflow_wrapper run -n`")
    
    return

def generate_project(bgcflow_dir, project_name, pep_version="2.1.0", use_project_rules=False,
                    samples_csv=False, prokka_db=False, gtdb_tax=False, description=False):
    """
    Generate a PEP project in BGCFlow config file:
    Params:
        - samples_csv
    """
    if bgcflow_dir is PosixPath:
        pass
    else:
        bgcflow_dir = Path(bgcflow_dir)
    global_config = bgcflow_dir / "config/config.yaml"
    template_dict = {'name': project_name,
                     'pep_version': pep_version,
                     'description': '<TO DO: give a description to your project>',
                     'sample_table': 'samples.csv',
                     'prokka-db': 'OPTIONAL: relative path to your `prokka-db.csv`',
                     'gtdb-tax': 'OPTIONAL: relative path to your `gtdbtk.bac120.summary.tsv`'
                    }
    if use_project_rules:
        with open(bgcflow_dir / "workflow/rules/rules.json", "r") as file:
            available_rules = json.load(file)
            available_rules = {rule : "FALSE" for rule in available_rules.keys()}
            template_dict['rules'] = available_rules
      
    project_dir = bgcflow_dir / f"config/{project_name}"
    project_dir.mkdir(parents=True, exist_ok=True)
    
    if type(samples_csv) == pd.core.frame.DataFrame:
        print("Generating samples file from Pandas DataFrame")
        assert samples_csv.index.name == 'genome_id'
        assert (samples_csv.columns == ['source', 'organism', 'genus', 'species', 'strain', 'closest_placement_reference']).all
        samples_csv.to_csv(project_dir / "samples.csv")
    elif type(samples_csv) == str:
        print(f"Copying samples file from {samples_csv}")
        samples_csv = Path(samples_csv)
        assert samples_csv.is_file()
        shutil.copy(samples_csv, project_dir / "samples.csv")
        
    if type(prokka_db) == str:
        print(f"Copying custom annotation file from {prokka_db}")
        prokka_db = Path(prokka_db)
        assert prokka_db.is_file()
        shutil.copy(prokka_db, project_dir / "prokka-db.csv")
        template_dict['prokka-db'] = "prokka-db.csv"
        
    if type(gtdb_tax) == str:
        print(f"Copying custom taxonomy from {gtdb_tax}")
        gtdb_tax = Path(gtdb_tax)
        assert gtdb_tax.is_file()
        shutil.copy(gtdb_tax, project_dir / "gtdbtk.bac120.summary.tsv")
        template_dict['gtdb-tax'] = "gtdbtk.bac120.summary.tsv"

    if type(description) == str:
        print(f"Writing project description...")
        template_dict['description'] = description
    
    print(f"Project config file generated in: {project_dir}")
    with open(project_dir / "project_config.yaml", "w") as file:
        yaml.dump(template_dict, file, sort_keys=False)
    
    if not global_config.is_file():
        bgcflow_init(bgcflow_dir, global_config)

    with open(bgcflow_dir / "config/config.yaml", "r") as file:
        print("Updating global config.yaml")
        main_config = yaml.safe_load(file)
        project_names = [p['name'] for p in main_config['projects']]
        assert project_name not in project_names, f"Project name: '{project_name}' already exists!\nUse a different name or edit the files in: {project_dir}"
        assert str(project_dir / "project_config.yaml") not in project_names, f"Project name: '{project_name}' already exists!\nUse a different name or edit the files in: {project_dir}"
        main_config['projects'].append({'name' : str(project_dir / "project_config.yaml")})
    
    with open(bgcflow_dir / "config/config.yaml", "w") as file:
        yaml.dump(main_config, file, sort_keys=False)
        
    return

def projects_util(**kwargs):
    pep_version = "2.1.0"
    bgcflow_dir = Path(kwargs["bgcflow_dir"]).resolve()
    config_dir = bgcflow_dir / 'config'
    config_dir.mkdir(parents=True, exist_ok=True)
    global_config = config_dir / "config.yaml"
    
    if type(kwargs['project']) == str:
        project_name = kwargs['project']
        
        generate_project(bgcflow_dir, kwargs['project'],
                         use_project_rules=kwargs['use_own_rules'], 
                         prokka_db=kwargs['prokka_db'],
                         gtdb_tax=kwargs['gtdb_tax'],
                         samples_csv=kwargs['samples_csv']
                        )
    else:
        bgcflow_init(bgcflow_dir, global_config)
    return

def copy_final_output(**kwargs):
    bgcflow_dir = Path(kwargs["bgcflow_dir"]).resolve()
    project_output = bgcflow_dir / f"data/processed/{kwargs['project']}"
    assert project_output.is_dir(), f"ERROR: Cannot find project [{kwargs['project']}] results. Run `bgcflow_wrapper init` to find available projects."
    subprocess.call(['rsync', '-avPhr', str(project_output), kwargs['copy']])
    return
