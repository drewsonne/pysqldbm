from dataclasses import dataclass
from enum import Enum, auto
from packaging.version import Version


class BranchType(Enum):
    FEATURE = auto()
    DEVELOP = auto()
    MAIN = auto()


@dataclass
class Release:
    """
    Collect the release version information and return the version string.

    Attributes:
        major (int | None): The major version number.
        minor (int | None): The minor version number.
        micro (int | None): The micro (patch) version number.
        rc (int | None): The release candidate number.
        alpha (int | None): The alpha version number.
        dev (int | None): The development build number.
        beta (int | None): The beta version number.

    Methods:
        version() -> Version:
            Return the version string ready for consumption by packaging.version.Version.
    """

    major: int | None = None
    minor: int | None = None
    micro: int | None = None
    rc: int | None = None
    alpha: int | None = None
    dev: int | None = None
    beta: int | None = None

    def version(self) -> Version:
        """
        Return the version string ready for consumption by packaging.version.Version.

        Constructs a version string based on the attributes of the Release object.
        The version string is formatted as "major.minor.micro" and may include
        additional segments for beta, release candidate, alpha, and development builds.

        Returns:
            Version: The constructed version string as a Version object.
        """
        v = f"{self.major}.{self.minor}.{self.micro}"
        if self.beta:
            v += f".b{self.beta}"
        elif self.rc:
            v += f".rc{self.rc}"
        elif self.alpha:
            v += f".a{self.alpha}.dev{self.dev}"

        return Version(v)


def bump_version(
    branch: BranchType,
    tag: str | None,
    build: int,
    pr: int,
    latest_release: Version,
    current_version: Version,
) -> Version:
    """
    Bump the version based on the branch type and where the current version is at.

    Args:
        branch (BranchType): The type of the branch (MAIN, DEVELOP, or FEATURE).
        tag (str | None): A specific version tag, if provided.
        build (int): The build number.
        pr (int): The pull request number.
        latest_release (Version): The latest released tag version from the main branch.
        current_version (Version): The current version of the software.

    Returns:
        Version: The next version of the software.
    """
    if branch == BranchType.MAIN:
        return _bump_version_main(tag, current_version)

    elif branch == BranchType.DEVELOP:
        return _bump_version_develop(latest_release, current_version)

    elif branch == BranchType.FEATURE:
        return _bump_version_feature(build, pr, latest_release, current_version)

    raise ValueError(f"Unknown branch type: {branch}")


def _bump_version_main(
    tag: str | None,
    current_version: Version,
) -> Version:
    """
    Determine the next version for the main branch.

    Args:
        tag (str | None): A specific version tag, if provided.
        current_version (Version): The current version of the software.

    Returns:
        Version: The next version of the software.

    If a tag is provided, this function returns the version corresponding to the tag.
    If no tag is provided, it checks if the current version has a pre-release segment.
    If the pre-release segment is a beta version, it sets the release candidate (rc) to 1.
    If the pre-release segment is a release candidate, it increments the rc number.
    Finally, it creates a new Release object with the current version's major, minor, and micro numbers,
    and the updated rc value if applicable, then returns the new version.
    """
    if tag:
        return Version(tag)

    rc = None
    if current_version.pre:
        if current_version.pre[0] == "b":
            rc = 1
        elif current_version.pre[0] == "rc":
            rc = current_version.pre[1] + 1
    return Release(
        major=current_version.major,
        minor=current_version.minor,
        micro=current_version.micro,
        rc=rc,
    ).version()


def _bump_version_develop(
    latest_release: Version,
    current_version: Version,
) -> Version:
    """
    Determine the next version for the develop branch.

    Args:
        latest_release (Version): The latest release version from the main branch.
        current_version (Version): The current version of the software.

    Returns:
        Version: The next version of the software.
    """
    if current_version >= latest_release:
        r = Release(
            current_version.major,
            current_version.minor,
            current_version.micro,
        )
        if current_version == latest_release:
            r.beta = 1
            r.micro += 1
        elif current_version.pre[0] == "b":  # If it's beta, just increment
            r.beta = current_version.pre[1] + 1
        else:
            r.beta = 1
        return r.version()
    return Release(
        latest_release.major,
        latest_release.minor,
        latest_release.micro + 1,
        beta=1,
    ).version()


def _bump_version_feature(
    build: int,
    pr: int,
    latest_release: Version,
    current_version: Version,
) -> Version:
    """
    Determine the next version for a feature branch.

    Args:
        build (int): The build number.
        pr (int): The pull request number.
        latest_release (Version): The latest release version from the main branch.
        current_version (Version): The current version of the software.

    Returns:
        Version: The next version of the software.

    This function creates a new Release object with the provided build and pull request numbers.
    If the current version is greater than the latest release, it sets the major, minor, and micro
    numbers based on the current version. If the current version has a pre-release segment and it is
    a beta version, it increments the micro number. Otherwise, it uses the micro number from the current version.
    If the current version is not greater than the latest release, it increments the micro number of the latest release.
    Finally, it returns the new version.
    """
    r = Release(dev=build, alpha=pr)
    # If we're in beta and the major and minor are the same, don't increment
    # the micro number
    if current_version.pre and current_version.pre[0] == "b":
        r.major, r.minor, r.micro = (
            current_version.major,
            current_version.minor,
            current_version.micro,
        )
    elif current_version > latest_release:
        r.major, r.minor, r.micro = (
            current_version.major,
            current_version.minor,
            (
                current_version.micro + 1
                if current_version.pre and current_version.pre[0] == "b"
                else current_version.micro
            ),
        )
    else:
        r.major, r.minor, r.micro = (
            latest_release.major,
            latest_release.minor,
            latest_release.micro + 1,
        )
    return r.version()


def get_branch_type(branch: str) -> BranchType:
    """
    Determine the type of branch based on its name.

    Args:
        branch (str): The name of the branch.

    Returns:
        BranchType: The type of the branch (MAIN, DEVELOP, or FEATURE).

    This function checks the name of the branch and returns the corresponding BranchType.
    - If the branch name is "main", it returns BranchType.MAIN.
    - If the branch name is "develop", it returns BranchType.DEVELOP.
    - For any other branch name, it returns BranchType.FEATURE.
    """
    if branch == "main":
        return BranchType.MAIN
    elif branch == "develop":
        return BranchType.DEVELOP
    else:
        return BranchType.FEATURE
