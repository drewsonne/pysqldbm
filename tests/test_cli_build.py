from packaging.version import Version
import pytest

from pysqldbm_cli.build import (
    bump_version_develop,
    bump_version_feature,
    bump_version_main,
)


@pytest.mark.parametrize(
    "build,pr,latest_release,current_version,expected_version",
    [
        (1, 1, "1.0.0", "1.0.0", "1.0.1a1.dev1"),
        (10, 43, "2.3.4", "3.0.0", "3.0.0a43.dev10"),
        (10, 20, "3.0.0", "3.0.1b10", "3.0.1a20.dev10"),
        (12, 7, "2.0.0", "1.0.0", "2.0.1a7.dev12"),
        (13, 8, "1.0.6", "1.0.7b5", "1.0.7a8.dev13"),
        # Test version progression
        (1, 1, "1.0.0", "1.0.0", "1.0.1a1.dev1"),
        # Test minor bump version progression
        (1, 1, "1.0.0", "1.1.0", "1.1.0a1.dev1"),
        # Test major bump version progress
        (1, 1, "1.0.0", "2.0.0", "2.0.0a1.dev1"),
    ],
)
def test_bump_version_feature(
    build: int,
    pr: int,
    latest_release: str,
    current_version: str,
    expected_version: str,
):
    actual_version = bump_version_feature(
        build,
        pr,
        Version(latest_release),
        Version(current_version),
    ).__str__()
    assert expected_version == actual_version


@pytest.mark.parametrize(
    "latest_release,current_version,expected_version",
    [
        ("1.0.0", "1.0.0", "1.0.1b1"),
        ("1.0.0", "1.0.1.b1", "1.0.1b2"),
        ("2.2.0", "2.0.1.a7.dev12", "2.2.1b1"),
        ("2.0.0", "2.0.1.a7.dev12", "2.0.1b1"),
        ("1.0.6", "1.0.7b2", "1.0.7b3"),
        ("1.0.0", "1.1.0a30.dev20", "1.1.0b1"),
        # Test version progression
        ("1.0.0", "1.0.1a1.dev1", "1.0.1b1"),
        # Test minor bump version progression
        ("1.0.0", "1.1.0a1.dev1", "1.1.0b1"),
        # Test major bump version progress
        ("1.0.0", "2.0.0a1.dev1", "2.0.0b1"),
    ],
)
def test_bump_version_develop(latest_release: str, current_version: str, expected_version: str):
    actual_version = bump_version_develop(
        Version(latest_release),
        Version(current_version),
    ).__str__()
    assert expected_version == actual_version


@pytest.mark.parametrize(
    "current_version,latest_version,expected_version",
    [
        ("1.0.1b1", "1.0.0", "1.0.1"),
        ("1.0.1b2", "1.0.0", "1.0.1"),
        ("2.2.1b1", "2.2.0", "2.2.1"),
        ("2.0.1b1", "2.0.0", "2.0.1"),
        ("1.0.7b3", "1.0.6", "1.0.7"),
        ("1.1.0b1", "1.0.0", "1.1.0"),
        ("1.1.0b1", "1.0.0", "1.1.0"),
        ("1.0.0", "1.0.1", "1.0.2"),
    ],
)
def test_bump_version_main(current_version: str, latest_version: str, expected_version: str):
    actual_version = bump_version_main(
        Version(latest_version),
        Version(current_version),
    ).__str__()
    assert expected_version == actual_version
