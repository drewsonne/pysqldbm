import os
import re
import subprocess
import sys
from pathlib import Path

SETUP_PY_PATH = Path(__file__).parent.parent / "setup.py"


def get_version_from_setup_py():
    with SETUP_PY_PATH.open("r") as f:
        content = f.read()
        version_match = re.search(r"version\s*=\s*['\"]([^'\"]*)['\"]", content)
        if version_match:
            return version_match.group(1)
    return None


def get_git_tag():
    try:
        return subprocess.check_output(["git", "describe", "--tags", "--exact-match"]).strip().decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def get_build_id() -> int:
    return int(os.environ.get("GITHUB_RUN_ID", "1658821493"))


def update_version_in_setup_py(version):
    with SETUP_PY_PATH.open("r") as f:
        content = f.read()

    new_content = re.sub(r"version\s*=\s*['\"][^'\"]*['\"]", f'version="{version}"', content)

    with SETUP_PY_PATH.open("w") as f:
        f.write(new_content)


def build_hash_semver(semver_version: str, git_hash: int) -> str:
    return f"{extract_semver(semver_version)}-dev{git_hash}"


def extract_semver(text):
    semver_pattern = r"^\b\d+\.\d+\.\d+"
    semver_match = re.search(semver_pattern, text)
    if semver_match:
        return semver_match.group()
    else:
        return None


if __name__ == "__main__":
    semver_version = get_version_from_setup_py()
    if not semver_version:
        print("Error: Could not find a valid semver version in setup.py.")
    else:
        git_tag = get_git_tag()
        if git_tag:
            update_version_in_setup_py(git_tag)
            print(f"Updated version in setup.py to use the git tag: {git_tag}")
        else:
            git_hash = get_build_id()
            new_version = build_hash_semver(semver_version, git_hash) if git_hash else semver_version
            update_version_in_setup_py(new_version)
            print(f"Updated version in setup.py to use the git hash: {new_version}")
