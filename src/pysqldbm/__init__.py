__all__ = ["client"]

from pysqldbm.client import Client


def client(api_key: str) -> "Client":
    return Client(api_key)
