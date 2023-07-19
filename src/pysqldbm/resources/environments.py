from typing import Generator

from pysqldbm.resources.base import BaseModel, BaseResources
from pysqldbm.rest_client import RestClient


class Environment(BaseModel):
    ...


class Environments(BaseResources):
    def __init__(self, client: RestClient, project_id: str, **kwargs):
        super().__init__(client, **kwargs)
        self._project_id = project_id

    def list(self) -> Generator[Environment, None, None]:
        """List all environments in a project"""
        yield from self._client.get_list(
            f"projects/{self._project_id}/environments", Environment
        )
