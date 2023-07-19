# pysqldm

A python API to wrap https://developers.sqldbm.com/.

## `sqldbm` CLI tool

### Installation
```bash
pip install sqldbm
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
pip install pysqldm
```

### Sample Usage with Client

```python
import pysqldbm

# Create a client
API_KEY = "your_api_key"
sqldbm = pysqldbm.client(API_KEY)

for project in sqldbm.projects.list():
    print(f"Show revisions for project '{project.name}'...")
    for revision in project.revisions.list():
        print(revision)
```

### Sample Usage with Resources

```python
from pysqldbm.resources.revisions import Revision

rev = Revision("project_id", "revision_id")
rev.fetch()

```