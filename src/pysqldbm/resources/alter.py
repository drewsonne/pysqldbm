from pysqldbm.resources.base import BaseModel, BaseResources
from pysqldbm.rest_client import RestClient


class Alter(BaseModel):
    def __init__(self, client: RestClient, project_id: str, **kwargs):
        super().__init__(client, **kwargs)
        self._project_id = project_id


class Alters(BaseResources):
    def __init__(self, client: RestClient, project_id: str):
        super().__init__(client)
        self._project_id = project_id

    def get(self) -> Alter:
        return self._client.get_one(f"projects/{self._project_id}/alter", Alter)

    def get_compare(
        self,
        revision_id: str,
        environment_id: str,
        with_revision_id: str,
        with_environment_id: str,
    ) -> Alter:
        return self._client.get_one(
            f"projects/{self._project_id}/alter/compare",
            Alter,
            query={
                "revision_id": revision_id,
                "environment_id": environment_id,
                "with_revision_id": with_revision_id,
                "with_environment_id": with_environment_id,
            },
        )
