from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from fastapi import FastAPI

from playground.core.services.classes.repository_in_memory_chooser import (
    InMemoryChooser,
)
from playground.core.services.classes.repositroy_sql_lite_chooser import SqlLiteChooser
from playground.core.services.classes.service_chooser import ServiceChooser
from playground.core.services.interfaces.currency_converter_interface import ICurrencyConverter
from playground.core.services.interfaces.memory.campaign_repository import CampaignRepository
from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.memory.product_repository import ProductRepository
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
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
from playground.infra.currency_converter.er_api_converter import ErApiConverter
from playground.infra.memory.in_memory.campaign_in_memory_repository import (
    CampaignInMemoryRepository,
)
from playground.infra.memory.in_memory.payment_in_memory_repository import (
    PaymentInMemoryRepository,
)
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.infra.memory.in_memory.receipts_in_memory_repository import (
    ReceiptInMemoryRepository,
)
from playground.infra.memory.in_memory.shift_in_memory_repository import ShiftInMemoryRepository

DB_NAME: Final = "shop.db"


@dataclass
class SetupConfiguration:
    service_chooser: IServiceChooser
    repository_chooser: IRepositoryChooser
    converter: ICurrencyConverter

    @classmethod
    def for_production(cls) -> SetupConfiguration:
        return cls(ServiceChooser(), SqlLiteChooser(DB_NAME), ErApiConverter())

    @classmethod
    def for_testing(
        cls,
        product_repo: ProductRepository = ProductInMemoryRepository(),
        shift_repo: ShiftRepository = ShiftInMemoryRepository(),
        receipt_repo: ReceiptRepository = ReceiptInMemoryRepository(),
        payment_repo: PaymentRepository = PaymentInMemoryRepository(),
        campaign_repo: CampaignRepository = CampaignInMemoryRepository(),
        converter: ICurrencyConverter = ErApiConverter(),
    ) -> SetupConfiguration:
        return cls(
            ServiceChooser(),
            InMemoryChooser(product_repo, shift_repo, receipt_repo, payment_repo, campaign_repo),
            converter,
        )


def set_up_routes(api: FastAPI) -> None:
    api.include_router(products_api, prefix="/products", tags=["Products"])
    api.include_router(receipts_api, prefix="/receipts", tags=["receipts"])
    api.include_router(payments_api, prefix="/payments", tags=["payments"])
    api.include_router(shifts_api, prefix="/shifts", tags=["shifts"])
    api.include_router(campaigns_api, prefix="/campaigns", tags=["campaigns"])
    api.include_router(sales_api, prefix="/sales", tags=["sales"])


def setup(setup_conf: SetupConfiguration) -> FastAPI:
    api = FastAPI()
    api.state.repo = setup_conf.repository_chooser
    api.state.core = setup_conf.service_chooser
    api.state.conv = setup_conf.converter
    set_up_routes(api)
    return api
