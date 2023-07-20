import pysqldbm.client


def client(api_key: str) -> "pysqldbm.client.Client":
    return pysqldbm.client.Client(api_key)
