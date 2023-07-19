from typing import Generator, Dict, Union

from pysqldbm.resources.alter import Alter, Alters
from pysqldbm.resources.base import BaseModel, BaseResources
from pysqldbm.resources.environments import Environments
from pysqldbm.resources.revisions import Revisions
from pysqldbm.rest_client import RestClient


class Project(BaseModel):
    def __init__(self, client: RestClient, project_id: str, **kwargs):
        super().__init__(client, **kwargs)
        self._project_id = project_id

    @property
    def revisions(self) -> Revisions:  # Generator[Revisions, None, None]:
        """Get the revisions resource for this project"""
        return Revisions(self._client, self._project_id)

    @property
    def alter(self) -> Alter:
        """Get the alter resource for this project"""
        return self._client.get_one(f"alter/{self._project_id}", Alter)


class Projects(BaseResources):
    def get(self, project_id: str) -> Project:
        """Get a project by id"""
        return Project(self._client, project_id)

    def list(self) -> Generator[Union[Project, Dict], None, None]:
        """List all projects"""
        yield from self._client.get_list("projects", Project)

    @property
    def environments(self) -> Environments:
        """Fetch the environments resource for this project"""
        return Environments(self._client, self._project_id)

    @property
    def alter_statements(self) -> Alters:
        """Fetch the alter statements resource for this project"""
        return Alters(self._client, self._project_id)
