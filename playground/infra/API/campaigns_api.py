from typing import List, Dict, Any
from fastapi import HTTPException
from fastapi import APIRouter
from starlette.requests import Request

from playground.core.models.campaign import Campaign
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import (
    ICampaignService,
)
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)

campaigns_api = APIRouter()


def get_campaign_service(request: Request) -> ICampaignService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_campaign_service(repository_chooser.get_campaign_repo())


@campaigns_api.get("")
async def get_campaign(request: Request) -> List[Campaign]:
    return get_campaign_service(request).get_all()


@campaigns_api.post("")
async def create_campaign(
    request: Request, campaign_type: str, params: Dict[str, Any]
) -> Campaign:
    service = get_campaign_service(request)
    return service.create(
        service.get_campaign_request_with_type_instance(campaign_type, **params)
    )


@campaigns_api.delete("/{campaign_id}")
async def delete_campaign(request: Request, campaign_id: str) -> None:
    print(campaign_id)
    try:
        get_campaign_service(request).delete(campaign_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
