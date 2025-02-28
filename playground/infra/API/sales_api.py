from fastapi import APIRouter
from starlette.requests import Request

from playground.core.models.sales import SalesItem
from playground.infra.API.payments_api import get_payment_service

sales_api = APIRouter()


@sales_api.get("/", status_code=201)
def get_sales(request: Request) -> list[SalesItem]:
    service = get_payment_service(request)
    return service.get_sales()
