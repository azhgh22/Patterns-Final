from playground.core.services.classes.payment_service import PaymentService
from playground.core.services.classes.campaign_service import CampaignService
from playground.core.services.classes.product_service import ProductService
from playground.core.services.classes.shift_service import ShiftService
from playground.core.services.classes.receipt_service import ReceiptService
from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.memory.campaign_repository import (
    CampaignRepository,
)
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.core.services.interfaces.service_interfaces.payments_service_interface import (
    IPaymentsService,
)
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import (
    ICampaignService,
)
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import (
    IReceiptService,
)
from playground.core.services.interfaces.service_interfaces.shift_service_interface import (
    IShiftService,
)


class ServiceChooser:
    def get_product_service(self, product_repo: ProductRepository) -> IProductService:
        return ProductService(product_repo)

    def get_campaign_service(self, campaign_repo: CampaignRepository) -> ICampaignService:
        return CampaignService(campaign_repo)

    def get_receipt_service(self, receipt_repo: ReceiptRepository) -> IReceiptService:
        return ReceiptService(receipt_repo)

    def get_shift_service(self, shift_repo: ShiftRepository) -> IShiftService:
        return ShiftService(shift_repo)

    def get_payment_service(self, payment_repo: PaymentRepository) -> IPaymentsService:
        return PaymentService(payment_repo)
