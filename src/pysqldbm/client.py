from pysqldbm.resources.projects import Projects
from pysqldbm.rest_client import RestClient


class Client:
    def __init__(self, api_key: str, return_dict: bool = False):
        self._rest_client = RestClient(
            api_key=api_key,
            base_url="https://api.sqldbm.com",
            return_dict=return_dict,
        )

    @property
    def projects(self) -> Projects:
        return Projects(self._rest_client)
