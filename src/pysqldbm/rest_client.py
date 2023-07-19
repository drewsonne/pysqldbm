from typing import Dict, Generator, Optional
from urllib.parse import urljoin

import backoff
import click
from requests import Session


class RateLimited(Exception):
    ...


def backoff_hdlr(details):
    click.echo(
        message=(
            "Backing off {wait:0.1f} seconds after {tries} tries "
            "calling function {target} with args {args} and kwargs "
            "{kwargs}"
        ).format(**details),
        err=True,
    )


class RestClient:
    """A client for the SQLDBM REST API."""

    def __init__(self, api_key: str, base_url: str):
        """
        :param api_key: The API key to use for authentication.
        :param base_url: The base URL of the SQLDBM API.
        """

        self._session = self.SessionWithUrlBase(
            url_base=base_url.rstrip("/") + "/"
        )  # Ensure we have a trailing slash, as urljoin() requires it.
        self._session.headers.update(
            {"accept": "application/json", "Authorization": api_key}
        )

    @backoff.on_exception(
        backoff.expo,
        (RateLimited,),
        on_backoff=backoff_hdlr,
        jitter=backoff.full_jitter,
    )
    def get(self, resource: str, query: Optional[Dict] = None) -> Dict:
        """Get a resource from the SQLDBM API."""
        response = self._session.get(resource, params=query)
        if response.status_code == 429:
            raise RateLimited(response.content)
        response.raise_for_status()

        return response.json()["data"]

    def get_raw(self, resource: str, query: Optional[Dict] = None) -> str:
        return self.get(resource, query=query)

    def get_one(self, resource: str) -> Dict:
        """Get a single resource from the SQLDBM API."""
        return self.get(resource)

    def get_list(self, resource: str) -> Generator[Dict, None, None]:
        """Get a list of resources from the SQLDBM API."""
        for result in self.get(resource):
            yield result

    class SessionWithUrlBase(Session):
        # Stolen from: https://stackoverflow.com/a/43882437
        # In Python 3 you could place `url_base` after `*args`, but not in Python 2.
        def __init__(self, *args, url_base=None, **kwargs):
            super(RestClient.SessionWithUrlBase,
                  self).__init__(*args, **kwargs)
            self.url_base = url_base

        def request(self, method: str, url: str, **kwargs):
            """Prepends the base URL to the resource passed in."""
            modified_url = urljoin(
                self.url_base, url.lstrip("/")
            )  # Remove leading slash, as urljoin() requires no leading slash.

            return super(RestClient.SessionWithUrlBase, self).request(
                method, modified_url, **kwargs
            )
