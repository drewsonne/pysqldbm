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

export SQLDB_API_KEY="your_api_key"
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
