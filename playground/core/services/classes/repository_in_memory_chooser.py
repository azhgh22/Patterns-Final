from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
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
        payment_repo: PaymentRepository = PaymentRepository(),
    ) -> None:
        self.product_repository = product_repo
        self.shift_repository = shift_repo
        self.receipt_repository = receipt_repo
        self.payment_repository = payment_repo

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository

    def get_shift_repository(self) -> ShiftRepository:
        return self.shift_repository

    def get_receipt_repo(self) -> ReceiptRepository:
        return self.receipt_repository

    def get_payment_repository(self) -> PaymentRepository:
        return self.payment_repository
