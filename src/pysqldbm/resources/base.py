from abc import abstractmethod, ABC

from pysqldbm.rest_client import RestClient


class BaseModel(ABC):
    def __init__(self, client: RestClient, **kwargs):
        self._client = client

        if len(kwargs):
            self._load_data(**kwargs)

    @abstractmethod
    def _load_data(self, **kwargs):
        ...
