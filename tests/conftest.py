import importlib
from pathlib import Path
from types import ModuleType

import pytest


@pytest.fixture(scope="module")
def project_pkg(project_name: str) -> ModuleType:
    return importlib.import_module(project_name)


@pytest.fixture(scope="module")
def project_name(pyproject_toml: Path) -> str:
    with open(file=pyproject_toml) as lines:
        for line in lines:
            if line.startswith("name"):
                name = line.split("=")[1].strip().strip('"')
                break

    return name


@pytest.fixture(scope="module")
def pyproject_toml(project_root: Path) -> Path:
    return project_root / "pyproject.toml"


@pytest.fixture(scope="module")
def project_root() -> Path:
    return Path(__file__).parent.parent.resolve()
