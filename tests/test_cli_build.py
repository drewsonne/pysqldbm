import pytest
from packaging.version import Version
from pysqldbm_cli.build import BranchType, bump_version, get_branch_type


@pytest.mark.parametrize(
    "name,expected_type",
    [
        ("main", BranchType.MAIN),
        ("develop", BranchType.DEVELOP),
        ("feature/some-feature", BranchType.FEATURE),
        ("other-feature", BranchType.FEATURE),
        ("master", BranchType.FEATURE),
    ],
)
def test_branch_type(name: str, expected_type: BranchType):
    assert get_branch_type(name) == expected_type


@pytest.mark.parametrize(
    "branch,tag,build,pr,latest_release,current_version,expected_version",
    [
        ("feature/other", "", 1, 1, "1.0.0", "1.0.0", "1.0.1a1.dev1"),
        ("other-feature", "4.0.0", 10, 43, "2.3.4", "3.0.0", "3.0.0a43.dev10"),
        ("mocked", "", 10, 20, "3.0.0", "3.0.1b10", "3.0.2a20.dev10"),
        ("nothing", "4.0.0", 12, 7, "2.0.0", "1.0.0", "2.0.1a7.dev12"),
        ("feature/other", "", 20, 30, "1.0.0", "1.1.0", "1.1.0a30.dev20"),
        ("develop", "", 1, 1, "1.0.0", "1.0.0", "1.0.1b1"),
        ("develop", "4.0.0", 1, 1, "1.0.0", "1.0.1.b1", "1.0.1b2"),
        ("develop", "", 1, 1, "2.2.0", "2.0.1.a7.dev12", "2.2.1b1"),
        ("develop", "4.0.0", 1, 1, "2.0.0", "2.0.1.a7.dev12", "2.0.1b1"),
        ("develop", "", "", "", "1.0.6", "1.0.7b2", "1.0.7b3"),
        ("develop", "", "", "", "1.0.0", "1.1.0a30.dev20", "1.1.0b1"),
        ("main", "", 20, 30, "1.0.0", "1.0.1b1", "1.0.1rc1"),
        ("main", "", 20, 30, "1.0.0", "1.0.1rc1", "1.0.1rc2"),
        ("main", "1.0.1", 20, 30, "1.0.0", "1.0.1rc1", "1.0.1"),
        ("main", "1.0.2", 20, 30, "1.0.0", "1.0.1rc1", "1.0.2"),
        # test version progression
        ("feature/other", "", 1, 1, "1.0.0", "1.0.0", "1.0.1a1.dev1"),
        ("develop", "", 1, 1, "1.0.0", "1.0.1a1.dev1", "1.0.1b1"),
        ("main", "", "", "", "1.0.0", "1.0.1b1", "1.0.1rc1"),
        ("main", "1.0.1", "", "", "1.0.0", "1.0.1rc1", "1.0.1"),
        # Test minor bump version progression
        ("feature/other", "", 1, 1, "1.0.0", "1.1.0", "1.1.0a1.dev1"),
        ("develop", "", 1, 1, "1.0.0", "1.1.0a1.dev1", "1.1.0b1"),
        ("main", "", "", "", "1.0.0", "1.1.0b1", "1.1.0rc1"),
        ("main", "1.1.0", "", "", "1.0.0", "1.1.0rc1", "1.1.0"),
    ],
)
def test_bump_version(
    branch: str,
    tag: str,
    build: int,
    pr: int,
    latest_release: str,
    current_version: str,
    expected_version: str,
):
    actual_version = bump_version(
        get_branch_type(branch),
        tag,
        build,
        pr,
        Version(latest_release),
        Version(current_version),
    ).__str__()
    assert expected_version == actual_version
