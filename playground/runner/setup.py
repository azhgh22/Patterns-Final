import enum
from dataclasses import dataclass

from fastapi import FastAPI

from playground.infra.API.products_api import products_api


class MemoryType(enum.Enum):
    IN_MEMORY = 0
    SQL_LITE = 1


@dataclass
class SetupConfiguration:
    memory_type: MemoryType

def set_up_rotes(api: FastAPI) -> None:
    api.include_router(products_api, prefix="/products", tags=["Products"])


def setup(setup_conf: SetupConfiguration) -> FastAPI:
    api = FastAPI()


    set_up_rotes(api)
    return api
