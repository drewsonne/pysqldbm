from typing import Generator


class Environment:
    def __init__(self):
        pass


class Environments:
    def __init__(self):
        pass

    def get(self) -> Environment:
        pass

    def list(self) -> Generator[Environment, None, None]:
        pass
