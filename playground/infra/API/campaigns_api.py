from typing import List, Optional

from fastapi import APIRouter, Query

from playground.core.models.receipt import ReceiptResponse

campaigns_api = APIRouter()


@campaigns_api.get("")
# todo: add return type
async def get_campaign():
    pass

@campaigns_api.post("")
# todo: add return type
async def create_campaign():
    pass

@campaigns_api.delete("/{campaign_id}")
# todo: add return type
async def delete_campaign(campaign_id: str):
    pass




