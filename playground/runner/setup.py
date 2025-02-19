import enum
from dataclasses import dataclass

from fastapi import FastAPI

from playground.infra.API.receipts_api import receipts_api
from playground.infra.API.products_api import products_api
from playground.infra.API.report_api import sales_api, x_reports_api


class MemoryType(enum.Enum):
    IN_MEMORY = 0
    SQL_LITE = 1


@dataclass
class SetupConfiguration:
    memory_type: MemoryType

def set_up_routes(api: FastAPI) -> None:
    api.include_router(products_api, prefix="/products", tags=["Products"])
    api.include_router(receipts_api, prefix="/receipts", tags=["Receipts"])
    api.include_router(sales_api, prefix="/sales", tags=["sales"])
    api.include_router(x_reports_api, prefix="/x-reports", tags=["x_reports"])


def setup(setup_conf: SetupConfiguration) -> FastAPI:
    api = FastAPI()


    set_up_routes(api)
    return api
