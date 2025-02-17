import enum
from dataclasses import dataclass

from fastapi import FastAPI


class MemoryType(enum.Enum):
    IN_MEMORY = 0
    SQL_LITE = 1


@dataclass
class SetupConfiguration:
    memory_type: MemoryType


def setup(setup_conf: SetupConfiguration) -> FastAPI:
    api = FastAPI()

    return api
