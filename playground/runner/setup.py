from dataclasses import dataclass

from fastapi import FastAPI

from playground.core.services.classes.repository_in_memory_chooser import (
    InMemoryChooser,
)
from playground.core.services.classes.repositroy_sql_lite_chooser import SqlLiteChooser
from playground.core.services.classes.repositroy_sql_lite_chooser import SqlLiteChooser
from playground.core.services.classes.service_chooser import ServiceChooser
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
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
from playground.infra.API.sales_api import sales_api
from playground.infra.API.shifts_api import shifts_api
from playground.infra.API.report_api import sales_api, x_reports_api
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)


@dataclass
class SetupConfiguration:
    service_chooser: IServiceChooser
    repository_chooser: IRepositoryChooser

    @classmethod
    def for_production(cls) -> "SetupConfiguration":
        return cls(ServiceChooser(), SqlLiteChooser())

    @classmethod
    def for_testing(
        cls, product_repo: ProductRepository = ProductInMemoryRepository()
    ) -> "SetupConfiguration":
        return cls(ServiceChooser(), InMemoryChooser(product_repo))


def set_up_routes(api: FastAPI) -> None:
    api.include_router(products_api, prefix="/products", tags=["Products"])
    api.include_router(receipts_api, prefix="/receipts", tags=["receipts"])
    api.include_router(payments_api, prefix="/payments", tags=["payments"])
    api.include_router(shifts_api, prefix="/shifts", tags=["shifts"])
    api.include_router(campaigns_api, prefix="/campaigns", tags=["campaigns"])
    api.include_router(sales_api, prefix="/sales", tags=["sales"])
    api.include_router(x_reports_api, prefix="/x-reports", tags=["x_reports"])


def setup(setup_conf: SetupConfiguration) -> FastAPI:
    api = FastAPI()
    api.state.repo = setup_conf.repository_chooser
    api.state.core = setup_conf.service_chooser
    set_up_routes(api)
    return api
