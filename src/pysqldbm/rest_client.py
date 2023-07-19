from typing import Dict, Generator
from urllib.parse import urljoin

from requests import Session


class RestClient:
    def __init__(self, api_key: str, base_url: str, return_dict: bool = False):
        self._return_dict = return_dict

        self._session = SessionWithUrlBase(
            url_base=base_url.rstrip("/") + "/"
        )  # Ensure we have a trailing slash, as urljoin() requires it.
        self._session.headers.update(
            {"accept": "application/json", "Authorization": api_key}
        )

    def get(
        self, resource: str, encapsulating_class: type, is_list: bool
    ) -> Generator[Dict, None, None]:
        response = self._session.get(resource)
        response.raise_for_status()

        result = response.json()["data"]
        if is_list:
            for item in result:
                if self._return_dict:
                    yield item  # Generator[Dict, None, None]
                else:
                    yield encapsulating_class(
                        self, item
                    )  # Generator[encapsulating_class, None, None]
        else:
            if self._return_dict:
                yield result
            else:
                yield encapsulating_class(self, result)


class SessionWithUrlBase(Session):
    # Stolen from: https://stackoverflow.com/a/43882437
    # In Python 3 you could place `url_base` after `*args`, but not in Python 2.
    def __init__(self, *args, url_base=None, **kwargs):
        super(SessionWithUrlBase, self).__init__(*args, **kwargs)
        self.url_base = url_base

    def request(self, method: str, url: str, **kwargs):
        modified_url = urljoin(
            self.url_base, url.lstrip("/")
        )  # Remove leading slash, as urljoin() requires no leading slash.

        return super(SessionWithUrlBase, self).request(method, modified_url, **kwargs)
