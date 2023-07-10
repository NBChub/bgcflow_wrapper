import shutil
import tempfile
import unittest
from pathlib import Path

import pandas as pd
import yaml

from bgcflow.bgcflow import cloner
from bgcflow.projects_util import generate_project


class TestGenerateProject(unittest.TestCase):
    def setUp(self):
        self.bgcflow_dir = Path(tempfile.mkdtemp())
        self.project_name = "test_project"
        self.pep_version = "2.1.0"
        self.use_project_rules = False
        self.samples_csv = pd.DataFrame(
            {
                "source": ["source1", "source2"],
                "organism": ["organism1", "organism2"],
                "genus": ["genus1", "genus2"],
                "species": ["species1", "species2"],
                "strain": ["strain1", "strain2"],
                "closest_placement_reference": ["ref1", "ref2"],
                "genome_id": ["genome1", "genome2"],
            }
        ).set_index("genome_id", inplace=True)
        self.prokka_db = self.bgcflow_dir / ".examples/_pep_example/prokka-db.csv"
        self.gtdb_tax = (
            self.bgcflow_dir / ".examples/_pep_example/gtdbtk.bac120.summary.tsv"
        )
        self.description = "Test project description"

        # Clone the bgcflow repository
        cloner(destination=self.bgcflow_dir, branch="main")

    def test_generate_project(self):
        generate_project(
            self.bgcflow_dir,
            self.project_name,
            self.pep_version,
            self.use_project_rules,
            self.samples_csv,
            self.prokka_db,
            self.gtdb_tax,
            self.description,
        )

        # Check if project directory and config file were created
        project_dir = self.bgcflow_dir / f"config/{self.project_name}"
        self.assertTrue(project_dir.is_dir())
        config_file = project_dir / "project_config.yaml"
        self.assertTrue(config_file.is_file())

        # Check if project config file contains the correct information
        with open(config_file, "r") as file:
            config_data = yaml.safe_load(file)
            print(config_data)
            self.assertEqual(config_data["name"], self.project_name)
            self.assertEqual(config_data["pep_version"], self.pep_version)
            self.assertEqual(config_data["description"], self.description)
            self.assertEqual(config_data["sample_table"], "samples.csv")
            self.assertEqual(
                config_data["prokka-db"],
                "OPTIONAL: relative path to your `prokka-db.csv`",
            )
            self.assertEqual(
                config_data["gtdb-tax"],
                "OPTIONAL: relative path to your `gtdbtk.bac120.summary.tsv`",
            )

        # Check if global config file was updated with the new project
        with open(self.bgcflow_dir / "config/config.yaml", "r") as file:
            config_data = yaml.safe_load(file)
            project_names = [p["name"] for p in config_data["projects"]]
            self.assertIn(str(config_file), project_names)

    def tearDown(self):
        # Remove test project directory and config file
        project_dir = self.bgcflow_dir / f"config/{self.project_name}"
        shutil.rmtree(project_dir)


if __name__ == "__main__":
    unittest.main()
