# pysqldm

A python API to wrap https://developers.sqldbm.com/.

## `pysqldbm` library

### Installation

```bash
pip install pysqldm
```

### Sample Usage with Client

```python
import pysqldbm

# Create a client
sqldbm = pysqldm.client()

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