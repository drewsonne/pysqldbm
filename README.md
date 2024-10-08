# pysqldbm

[![PyPI Version](https://img.shields.io/pypi/v/pysqldbm.svg)](https://pypi.python.org/pypi/pysqldbm)

A python API to wrap https://developers.sqldbm.com/.

## `sqldbm` CLI tool

### Installation

```bash
pip install pysqldbm[cli]
```

### Usage

```bash
sqldbm --help

export SQLDBM_API_KEY="your_api_key"
sqldbm list-projects # or `sqldbm --api-key="your_api_key" list-projects`
```

## `pysqldbm` library

### Installation

```bash
pip install pysqldbm
```

If you would like to use the latest overnight builds, you can install from test pypi

```bash
pip install -i https://test.pypi.org/simple/ pysqldbm
```

### Sample Usage with Client

```python
import pysqldbm

# Create a client
API_KEY = "your_api_key"
sqldbm = pysqldbm.client(API_KEY)

for project in sqldbm.list_projects():
    print(f"Show revisions for project '{project['name']}'...")
    for revision in sqldbm.list_revisions(project['id']):
        print(revision)
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md).

## Release Versioning

### Feature Branch

${MAJOR}.${MINOR}.${PATCH}.pre${PR_NUMBER}.dev${BUILD_NUMBER}

### Beta

When pushing into the develop branch, the following conditions are evaluated:

- If the develop version is ahead of the latest release version, use the develop version, and set the beta version to 1
- If the develop version is not ahead of the latest use the develop version, and increment the beta version

This is handled in the `.github/workflows/beta-version-bump.yml`.
