from dataclasses import dataclass

from fastapi import FastAPI

from playground.core.services.classes.repository_in_memory_chooser import (
    InMemoryChooser,
)
from playground.core.services.classes.repositroy_sql_lite_chooser import SqlLiteChooser
from playground.core.services.classes.service_chooser import ServiceChooser
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)
from playground.infra.API.campaigns_api import campaigns_api
from playground.infra.API.payments_api import payments_api
from playground.infra.API.products_api import products_api
from playground.infra.API.receipts_api import receipts_api
from playground.infra.API.shifts_api import shifts_api


@dataclass
class SetupConfiguration:
    service_chooser: IServiceChooser = ServiceChooser()
    repository_chooser: IRepositoryChooser = SqlLiteChooser()


def set_up_routes(api: FastAPI) -> None:
    api.include_router(products_api, prefix="/products", tags=["Products"])
    api.include_router(receipts_api, prefix="/receipts", tags=["receipts"])
    api.include_router(payments_api, prefix="/payments", tags=["payments"])
    api.include_router(shifts_api, prefix="/shifts", tags=["shifts"])
    api.include_router(campaigns_api, prefix="/campaigns", tags=["campaigns"])


def setup(setup_conf: SetupConfiguration) -> FastAPI:
    api = FastAPI()
    api.state.repo = setup_conf.repository_chooser
    api.state.core = setup_conf.service_chooser
    set_up_routes(api)
    return api
