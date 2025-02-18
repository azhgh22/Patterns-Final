from typing import List, Optional

from fastapi import APIRouter, Query

from playground.core.models.receipt import ReceiptResponse

sales_api = APIRouter()
x_reports_api = APIRouter()


@sales_api.get("")
async def get_sales_summary()-> List[ReceiptResponse]:
    pass

@x_reports_api.get("")
async def get_receipts_by_shift_id(shift_id: Optional[int] = Query(None)) -> List[ReceiptResponse]:
    pass

