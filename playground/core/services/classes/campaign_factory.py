from playground.core.models.campaign import (
    BuyNGetNCampaignRequest,
    DiscountCampaignRequest,
    CampaignRequestInterface,
    ComboCampaignRequest,
)
from playground.core.services.classes.campaign_classes import (
    BuyNGetNCampaign,
    DiscountCampaign,
    ComboCampaign,
    CampaignInterface,
)


class CampaignFactory:
    CAMPAIGN_TYPES = {
        "buy_n_get_n": BuyNGetNCampaign,
        "discount": DiscountCampaign,
        "combo": ComboCampaign,
    }

    @staticmethod
    def create_campaign(campaign_type: str, **kwargs) -> CampaignInterface:
        campaign_class = CampaignFactory.CAMPAIGN_TYPES.get(campaign_type)
        if not campaign_class:
            raise ValueError(f"Invalid campaign type: {campaign_type}")
        return campaign_class.create(**kwargs)


class CampaignRequestFactory:
    CAMPAIGN_REQUEST_TYPES = {
        "buy_n_get_n": BuyNGetNCampaignRequest,
        "discount": DiscountCampaignRequest,
        "combo": ComboCampaignRequest,
    }

    @staticmethod
    def create_campaign(campaign_type: str, **kwargs) -> CampaignRequestInterface:
        campaign_request_class = CampaignRequestFactory.CAMPAIGN_REQUEST_TYPES.get(
            campaign_type
        )
        if not campaign_request_class:
            raise ValueError(f"Invalid campaign type: {campaign_type}")
        return campaign_request_class.create(**kwargs)
