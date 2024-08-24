from dataclasses import dataclass
from packaging.version import Version


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

    major: int
    minor: int
    micro: int
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


def bump_version_main(
    latest_version: Version,
    current_version: Version,
) -> Version:
    return (
        Release(
            current_version.major,
            current_version.minor,
            current_version.micro,
        )
        if current_version > latest_version
        else Release(
            latest_version.major,
            latest_version.minor,
            latest_version.micro + 1,
        )
    ).version()


def bump_version_develop(
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


def bump_version_feature(
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
    r = Release(0, 0, 0, dev=build, alpha=pr)
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
