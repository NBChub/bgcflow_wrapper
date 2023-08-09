import toml

import bgcflow


def test_version():
    """Check if version in pyproject.toml and __init__.py match"""
    toml_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
    wrapper_version = bgcflow.__version__
    assert (
        toml_version == wrapper_version
    ), "Version mismatch between pyproject.toml and bgcflow/__init__.py"
