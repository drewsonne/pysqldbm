def client(api_key: str) -> "pysqldbm.Client":
    from pysqldbm.client import Client

    return Client(api_key)
