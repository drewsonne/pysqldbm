from abc import ABC
from typing import Generator

from pysqldbm.resources.base import BaseModel
from pysqldbm.resources.ddl import Ddl, DDLs
from pysqldbm.rest_client import RestClient


class Revision(BaseModel):

    def __init__(self, client: RestClient, project_id: str, revision_id: str, **kwargs):
        super().__init__(client)
        self._project_id = project_id
        self._revision_id = revision_id

        self._load_data(**kwargs)

    @property
    def ddls(self) -> DDLs:
        return DDLs(self._client, self._project_id, self._revision_id)


class Revisions(BaseModel):
    def __init__(self, client: RestClient, project_id: str):
        super().__init__(client)
        self._project_id = project_id

    def get(self, revision_id: str) -> Revision:
        yield from self._client.get_one(f"revisions/{self._project_id}/revisions/{revision_id}", Revision)

    def list(self) -> Generator[Revision, None, None]:
        yield from self._client.get_list(f"revisions/{self._project_id}", Revisions)

    def last(self) -> Revision:
        yield from self.get("last")
