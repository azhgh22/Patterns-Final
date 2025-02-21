from playground.core.services.classes.product_service import ProductService
from playground.core.services.classes.receipt_service import ReceiptService
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import IReceiptService


class ServiceChooser:
    def get_product_service(self, product_repo: ProductRepository) -> IProductService:
        return ProductService(product_repo)

    def get_receipt_service(self, receipt_repo: ReceiptRepository) -> IReceiptService:
        return ReceiptService(receipt_repo)
