"""Test the CLI."""

import importlib.metadata
from pathlib import Path

from click.testing import CliRunner

from nrl_test_data_generator.cli import cli


def test_cli_with_version() -> None:
    """Should result in exit code 0 and two files with 4 elements."""
    expected_version_no_cli = importlib.metadata.version("nrl-test-data-generator")

    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0, result.output

    # Check that two files are created
    assert (f"nrl-test-data-generator, {expected_version_no_cli}\n") == result.output


def test_cli_with_no_options() -> None:
    """Should result in exit code 0 and two files with 4 elements."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli)
        assert result.exit_code == 0, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 2, f"Expected 2 files, found {len(files)}"


def test_cli_with_total_elements_8() -> None:
    """Should result in exit code 0 and two files with 8 elements."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--total-elements", "8"])
        assert result.exit_code == 0, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_8_elements_*.*"))
        assert len(files) == 2, f"Expected 2 files, found {len(files)}"


def test_cli_with_region() -> None:
    """Should result in exit code 0 and two files with 4 elements."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--region", "Oslo_area"])
        assert result.exit_code == 0, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 2, f"Expected 2 files, found {len(files)}"


def test_cli_with_include_errors() -> None:
    """Should result in exit code 0 and two files with 4 elements."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--include-errors"])
        assert result.exit_code == 0, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 2, f"Expected 2 files, found {len(files)}"


def test_cli_with_exclude_errors() -> None:
    """Should result in exit code 0 and two files with 4 elements."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--exclude-errors"])
        assert result.exit_code == 0, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 2, f"Expected 2 files, found {len(files)}"


def test_cli_with_error_freq() -> None:
    """Should result in exit code 0 and three files with 4 elements."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--error-freq", "0.2"])
        assert result.exit_code == 0, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 2 or 3, f"Expected 2 or 3 files, found {len(files)}"


def test_cli_with_error_freq_gt_1() -> None:
    """Should result in exit code 1 and no files."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--error-freq", "1.2"])
        assert result.exit_code == 1, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 0, f"Expected 0 files, found {len(files)}"


def test_cli_with_error_pos() -> None:
    """Should result in exit code 0 and two files with 4 elements."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--error-pos", "1,3"])
        assert result.exit_code == 0, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 3, f"Expected 3 files, found {len(files)}"


def test_cli_with_faulty_error_pos() -> None:
    """Should result in exit code 1 and no files."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--error-pos", "1.3"])
        assert result.exit_code == 1, result.output

        # Check that two files are created
        files = list(Path().glob("testdata_4_elements_*.*"))
        assert len(files) == 0, f"Expected 0 files, found {len(files)}"
