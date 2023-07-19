from typing import Generator

from pysqldbm.models.ddl import Ddl


class Revision:
    def __init__(self):
        pass


class Revisions:
    def __init__(self):
        pass

    def get(self, revision_id: str) -> Revision:
        pass

    def list(self) -> Generator[Revision, None, None]:
        pass

    @property
    def last(self) -> Revision:
        pass

    @property
    def ddl(self) -> Ddl:
        pass
