# pysqldm

A python API to wrap https://developers.sqldbm.com/.

## `sqldbm` CLI tool

### Installation

```bash
git clone git@github.com:drewsonne/pysqldbm.git
cd pysqldbm
pip install -e .[cli]
```

### Usage

```bash
sqldb --help

export SQLDB_API_KEY="your_api_key"
sqldbm list-projects # or `sqldbm --api-key="your_api_key" list-projects`
```

## `pysqldbm` library

### Installation

```bash
git clone git@github.com:drewsonne/pysqldbm.git
cd pysqldbm
pip install -e .
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
