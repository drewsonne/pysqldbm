from typing import Generator, Dict, Union

from pysqldbm.resources.alter import Alter, Alters
from pysqldbm.resources.base import BaseModel
from pysqldbm.resources.environments import Environments
from pysqldbm.resources.revisions import Revisions
from pysqldbm.rest_client import RestClient


class Project(BaseModel):
    def __init__(self, client: RestClient, project_id: str):
        super().__init__(client)
        self._project_id = project_id

    @property
    def revisions(self) -> Revisions:  # Generator[Revisions, None, None]:
        return Revisions(self._client, self._project_id)

    @property
    def alter(self) -> Alter:
        return self._client.get_one(f"alter/{self._project_id}", Alter)


class Projects(BaseModel):
    def get(self, project_id: str) -> Project:
        return Project(self._client, project_id)

    def list(self) -> Generator[Union[Project, Dict], None, None]:
        yield from self._client.get_list("projects", Project)

    @property
    def environments(self) -> Environments:
        return Environments(self._client, self._project_id)

    @property
    def alter_statements(self) -> Alters:
        return Alters(self._client, self._project_id)
