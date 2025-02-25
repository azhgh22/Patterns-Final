from typing import Protocol

from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.memory.campaign_repository import CampaignRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository


class IRepositoryChooser(Protocol):
    def get_product_repo(self) -> ProductRepository:
        pass

    def get_campaign_repo(self) -> CampaignRepository:
        pass

    def get_receipt_repo(self) -> ReceiptRepository:
        pass

    def get_shift_repo(self) -> ShiftRepository:
        pass

    def get_payment_repo(self) -> PaymentRepository:
        pass
