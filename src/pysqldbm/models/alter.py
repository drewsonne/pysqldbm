from typing import Generator

from pysqldbm.models.base import BaseModel
from pysqldbm.models.compare import Compare


class Alter(BaseModel):
    @property
    def compare(self) -> Compare:
        pass
