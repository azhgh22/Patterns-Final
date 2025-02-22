from typing import Protocol

from playground.core.services.interfaces.memory import ShiftRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)
from playground.core.services.interfaces.service_interfaces.shift_service_interface import (
    IShiftService,
)
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import (
    IReceiptService,
)


class IServiceChooser(Protocol):
    def get_product_service(self, product_repo: ProductRepository) -> IProductService:
        pass

    def get_receipt_service(self, receipt_repo: ReceiptRepository) -> IReceiptService:
        pass


    def get_shift_service(self, shift_repo: ShiftRepository) -> IShiftService:
        pass
