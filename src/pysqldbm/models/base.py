from pysqldbm.rest_client import RestClient


class BaseModel:
    def __init__(self, client: RestClient):
        self._client = client
