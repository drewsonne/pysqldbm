from functools import partial
from typing import Callable, List
import pytest
from click.testing import CliRunner, Result

CLITestRunner = Callable[[List[str]], Result]


@pytest.fixture(scope="module")
def cli_runner() -> CLITestRunner:
    from pysqldbm_cli.run import run

    runner = CliRunner()
    return partial(runner.invoke, run, catch_exceptions=False)


def test_feature_branch(cli_runner: CLITestRunner):
    result = cli_runner(
        [
            "build",
            "version-bump",
            "feature",
            "--build",
            "1",
            "--pr",
            "1",
            "--current-version",
            "1.0.0",
            "--latest-release",
            "1.0.0",
        ]
    )
    assert result.exit_code == 0
    assert result.stdout == "1.0.1a1.dev1\n"


def test_develop_branch(cli_runner: CLITestRunner):
    result = cli_runner(
        [
            "build",
            "version-bump",
            "develop",
            "--current-version",
            "1.0.7b2",
            "--latest-release",
            "1.0.6",
        ]
    )
    assert result.exit_code == 0
    assert result.stdout == "1.0.7b3\n"


def test_main_branch(cli_runner: CLITestRunner):
    result = cli_runner(
        [
            "build",
            "version-bump",
            "main",
            "--current-version",
            "1.0.7b3",
            "--latest-release",
            "1.0.6",
        ]
    )
    assert result.exit_code == 0
    assert result.stdout == "1.0.7\n"
