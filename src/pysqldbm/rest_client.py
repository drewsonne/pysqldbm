from typing import Dict, Generator, Union, Type, TypeVar, Optional
from urllib.parse import urljoin

from requests import Session

from pysqldbm.resources.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class RestClient:
    """A client for the SQLDBM REST API."""

    def __init__(self, api_key: str, base_url: str, return_dict: bool = False):
        """
        :param api_key: The API key to use for authentication.
        :param base_url: The base URL of the SQLDBM API.
        :param return_dict: Whether to return dictionaries instead of models.
        """
        self._return_dict = return_dict

        self._session = SessionWithUrlBase(
            url_base=base_url.rstrip("/") + "/"
        )  # Ensure we have a trailing slash, as urljoin() requires it.
        self._session.headers.update(
            {"accept": "application/json", "Authorization": api_key}
        )

    def get(self, resource: str, query: Optional[Dict] = None) -> Dict:
        """Get a resource from the SQLDBM API."""
        response = self._session.get(resource, params=query)
        response.raise_for_status()

        return response.json()["data"]

    def get_one(
        self, resource: str, encapsulating_class: Type[T], query: Optional[Dict] = None
    ) -> Union[Dict, T]:
        """Get a single resource from the SQLDBM API."""
        result = self.get(resource, query=query)
        return encapsulating_class(self, **result) if not self._return_dict else result

    def get_list(
        self, resource: str, encapsulating_class: Type[T]
    ) -> Generator[Union[Dict, T], None, None]:
        """Get a list of resources from the SQLDBM API."""
        for result in self.get(resource):
            yield encapsulating_class(
                self, **result
            ) if not self._return_dict else result


class SessionWithUrlBase(Session):
    # Stolen from: https://stackoverflow.com/a/43882437
    # In Python 3 you could place `url_base` after `*args`, but not in Python 2.
    def __init__(self, *args, url_base=None, **kwargs):
        super(SessionWithUrlBase, self).__init__(*args, **kwargs)
        self.url_base = url_base

    def request(self, method: str, url: str, **kwargs):
        """Prepends the base URL to the resource passed in."""
        modified_url = urljoin(
            self.url_base, url.lstrip("/")
        )  # Remove leading slash, as urljoin() requires no leading slash.

        return super(SessionWithUrlBase, self).request(method, modified_url, **kwargs)
