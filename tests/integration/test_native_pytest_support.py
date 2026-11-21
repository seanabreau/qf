"""Public contract of the pytest versions accepted by the native pytest route."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.support import VfyProject
from tests.support.platforms import requires_native_pytest

pytestmark = requires_native_pytest


def _project_reporting_pytest_version(tmp_path: Path, version: str) -> tuple[VfyProject, str]:
    """Return a project whose distribution metadata names ``version`` for pytest."""

    project = VfyProject(tmp_path)
    project.write("test_case.py", "def test_case():\n    assert True\n")
    project.write(
        f"fake-metadata/pytest-{version}.dist-info/METADATA",
        f"Metadata-Version: 2.1\nName: pytest\nVersion: {version}\n",
    )
    return project, str(tmp_path / "fake-metadata")


@pytest.mark.parametrize("installed", ["7.4.4", "8.5.0", "9.2.1", "9.3.0", "9.2.0rc1", "10.0.0"])
def test_native_engine_reports_unsupported_pytest_version_actionably(
    tmp_path: Path, installed: str
) -> None:
    project, metadata = _project_reporting_pytest_version(tmp_path, installed)

    result = project.run_vfy(
        "test", "--engine=native", "--no-cov", "-q", env={"PYTHONPATH": metadata}
    )

    result.expect(1)
    assert (
        f"supports stable pytest >=8.0,<8.5 or >=9.0,<=9.2.0; found pytest {installed}"
        in result.stderr
    )
    assert "passed" not in result.stdout


@pytest.mark.parametrize("installed", ["8.0.0", "8.4.2", "9.0.0", "9.1.1", "9.2.0"])
def test_native_engine_accepts_supported_pytest_versions(tmp_path: Path, installed: str) -> None:
    project, metadata = _project_reporting_pytest_version(tmp_path, installed)

    result = project.run_vfy(
        "test", "--engine=native", "--no-cov", "-q", env={"PYTHONPATH": metadata}
    )

    assert "found pytest" not in result.stderr
    result.expect(0)
    assert "1 passed" in result.stdout
