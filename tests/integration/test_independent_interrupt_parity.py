"""Interrupt and exit banners that pytest's terminal reporter writes at session finish."""

from __future__ import annotations

from pathlib import Path

from tests.support import VfyProject
from tests.support.differential import run_matching
from tests.support.platforms import requires_native_pytest

pytestmark = requires_native_pytest


def test_keyboard_interrupt_in_test_prints_stock_banner(tmp_path: Path) -> None:
    project = VfyProject(tmp_path)
    project.write("test_interrupt.py", "def test_interrupt():\n    raise KeyboardInterrupt\n")

    result = run_matching(project)

    assert result.returncode == 2
    assert "!!!!! KeyboardInterrupt !!!!!" in result.stdout
    assert "(to show a full traceback on KeyboardInterrupt use --full-trace)" in result.stdout


def test_pytest_exit_in_test_prints_stock_banner(tmp_path: Path) -> None:
    project = VfyProject(tmp_path)
    project.write("test_exit.py", "import pytest\n\n\ndef test_exit():\n    pytest.exit('bye')\n")

    result = run_matching(project)

    assert result.returncode == 2
    assert "!!!!! _pytest.outcomes.Exit: bye !!!!!" in result.stdout
