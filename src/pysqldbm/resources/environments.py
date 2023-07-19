from typing import Generator

from pysqldbm.resources.base import BaseModel
from pysqldbm.rest_client import RestClient


class Environment(BaseModel):
    ...


class Environments(BaseModel):
    def __init__(self, client: RestClient, project_id: str):
        super().__init__(client)
        self._project_id = project_id

    def list(self) -> Generator[Environment, None, None]:
        yield from self._client.get_list(f"projects/{self._project_id}/environments", Environment)
