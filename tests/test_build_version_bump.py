from functools import partial
from textwrap import dedent
from typing import Callable, List
import pytest
from click.testing import CliRunner, Result

CLITestRunner = Callable[[List[str]], Result]


@pytest.fixture(scope="module")
def cli_runner() -> CLITestRunner:
    from pysqldbm_cli.run import run

    runner = CliRunner()
    return partial(runner.invoke, run, catch_exceptions=False)


@pytest.mark.parametrize(
    "branch,options,expected_output",
    [
        (
            "feature/branch",
            "--build 1 --pr 1 --tag " " --current-version 1.0.0 --latest-release 1.0.0",
            "1.0.1a1.dev1\n",
        ),
        ("develop", "--current-version 1.0.7b2 --latest-release 1.0.6", "1.0.7b3\n"),
    ],
)
def test_feature_branch(cli_runner: CLITestRunner, branch: str, options: str, expected_output: str):
    result = cli_runner(["build", "version-bump", "--branch", branch] + options.split(" "))
    result.return_value == 0
    assert result.stdout == expected_output
