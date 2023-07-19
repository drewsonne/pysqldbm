import json
from abc import abstractmethod, ABC
from typing import Dict

from pysqldbm.rest_client import RestClient


class BaseModel(ABC):
    """Base class for all models."""

    def __init__(self, client: RestClient, **kwargs):
        """
        :param client: The client to use for API calls.
        :param kwargs: The data to load into the model.
        """
        self._client = client

        if len(kwargs):
            self._load_data(**kwargs)

    @abstractmethod
    def _load_data(self, **kwargs):
        ...

    def as_dict(self) -> Dict:
        """Return the model as a dictionary."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def as_json(self) -> str:
        """Return the model as a JSON string."""
        return json.dumps(self.as_dict(), indent=4, sort_keys=True)


class BaseResources(BaseModel):
    """Base class for all resources."""

    def _load_data(self, **kwargs):
        ...
