from typing import Generator, Dict, Union

from pysqldbm.models.alter import Alter
from pysqldbm.models.base import BaseModel
from pysqldbm.models.environments import Environments
from pysqldbm.models.revisions import Revisions
from pysqldbm.rest_client import RestClient


class Project(BaseModel):
    def __init__(self, client: RestClient, project_id: str):
        super().__init__(client)
        self._project_id = project_id

    @property
    def revisions(self) -> Generator[Revisions, None, None]:
        yield from self._client.get(
            f"revisions/{self._project_id}", Revisions, is_list=True
        )

    @property
    def alter(self) -> Alter:
        return next(self._client.get(f"alter/{self._project_id}", Alter, is_list=False))


class Projects(BaseModel):
    def get(self, project_id: str) -> Project:
        return Project(self._client, project_id)

    def list(self) -> Generator[Union[Project, Dict], None, None]:
        yield from self._client.get("projects", Project, is_list=True)

    @property
    def environments(self) -> Environments:
        pass
