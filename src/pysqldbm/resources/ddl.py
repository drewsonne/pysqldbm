from pysqldbm.resources.base import BaseModel, BaseResources
from pysqldbm.rest_client import RestClient


class DDL(BaseModel):
    def __init__(self, client: RestClient, project_id: str, revision_id: str, **kwargs):
        super().__init__(client, **kwargs)
        self._project_id = project_id
        self._revision_id = revision_id


class DDLs(BaseResources):
    def __init__(self, client: RestClient, project_id: str, revision_id: str):
        super().__init__(client)
        self._project_id = project_id
        self._revision_id = revision_id

    def get(self) -> DDL:
        """Get the DDL of a revision."""
        return self._client.get_one(
            f"projects/{self._project_id}/revisions/{self._revision_id}/ddl", DDL
        )
