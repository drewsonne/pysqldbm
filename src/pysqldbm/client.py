from typing import Dict, Generator

from pysqldbm.rest_client import RestClient


class Client:
    BASE_URL = "https://api.sqldbm.com"

    def __init__(self, api_key: str):
        self._rest = RestClient(api_key=api_key, base_url=self.BASE_URL)

    def list_projects(self) -> Generator[Dict, None, None]:
        return self._rest.get_list("projects")

    def list_revisions(self, project_id: str) -> Generator[Dict, None, None]:
        return self._rest.get_list(f"projects/{project_id}/revisions")

    def get_revision(self, project_id: str, revision_id: str) -> Dict:
        return self._rest.get_one(f"projects/{project_id}/revisions/{revision_id}")

    def get_last_revision(self, project_id: str) -> Dict:
        return self.get_revision(project_id, "last")

    def get_ddl(self, project_id: str, revision_id: str) -> Dict:
        return self._rest.get_one(f"projects/{project_id}/revisions/{revision_id}/ddl")

    def get_last_ddl(self, project_id: str) -> Dict:
        return self.get_ddl(project_id, "last")

    def list_environments(self, project_id: str) -> Generator[Dict, None, None]:
        return self._rest.get_list(f"projects/{project_id}/environments")

    def get_latest_alter_statement(self, project_id: str) -> str:
        return self._rest.get_one(f"projects/{project_id}/alter")

    def get_alter_statement(
        self,
        project_id: str,
        revision_id: str,
        environment_id: str,
        with_revision_id: str,
        with_environment_id: str,
    ) -> str:
        return self._rest.get_raw(
            f"projects/{project_id}/alter/compare",
            query={
                "revision_id": revision_id,
                "environment_id": environment_id,
                "with_revision_id": with_revision_id,
                "with_environment_id": with_environment_id,
            },
        )

    def get_latest_object_ddl(self, project_id: str, object_name: str, case_sensitive: bool = False) -> str:
        return self._rest.get_raw(
            f"projects/{project_id}/revisions/last/objects/ddl",
            query={"name": object_name, "caseSensitive": case_sensitive},
        )

    def get_object_ddl(self, project_id: str, revision_id: str, object_name: str, case_sensitive: bool = False) -> str:
        return self._rest.get_raw(
            f"projects/{project_id}/revisions/{revision_id}/objects/ddl",
            query={"name": object_name, "caseSensitive": case_sensitive},
        )
