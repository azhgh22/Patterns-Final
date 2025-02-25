from playground.core.services.interfaces.memory.campaign_repository import (
    CampaignRepository,
)
from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.infra.memory.in_memory.campaign_in_memory_repository import (
    CampaignInMemoryRepository,
)
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)
from playground.infra.memory.in_memory.payment_in_memory_repository import (
    PaymentInMemoryRepository,
)
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.infra.memory.in_memory.shift_in_memory_repository import (
    ShiftInMemoryRepository,
)
from playground.infra.memory.in_memory.receipts_in_memory_repository import (
    ReceiptInMemoryRepository,
)


class InMemoryChooser:
    def __init__(
        self,
        product_repo: ProductRepository = ProductInMemoryRepository(),
        shift_repo: ShiftRepository = ShiftInMemoryRepository(),
        receipt_repo: ReceiptRepository = ReceiptInMemoryRepository(),
        payment_repo: PaymentRepository = PaymentInMemoryRepository(),
        campaign_repo: CampaignRepository = CampaignInMemoryRepository(),
    ) -> None:
        self.product_repository = product_repo
        self.shift_repository = shift_repo
        self.receipt_repository = receipt_repo
        self.payment_repository = payment_repo
        self.campaign_repository = campaign_repo

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository

    def get_shift_repo(self) -> ShiftRepository:
        return self.shift_repository

    def get_receipt_repo(self) -> ReceiptRepository:
        return self.receipt_repository

    def get_payment_repo(self) -> PaymentRepository:
        return self.payment_repository

    def get_campaign_repo(self) -> CampaignRepository:
        return self.campaign_repository
