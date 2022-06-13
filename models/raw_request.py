from pydantic import BaseModel


class RawRequest(BaseModel):
    # Received from partner
    created: str = None
    offer_id: str = None
    source: str = None
    aff_sub1: str = None
    aff_sub2: str = None
    aff_sub3: str = None
    aff_sub4: str = None
    aff_sub5: str = None
    status: str = None
    sum: str = None
    partner: str = None
    partner_account_id: str = None
    conversion_id: str = None
    type_event: str = None
    payout: str = None
    currency: str = None

    adids: str = None # advertisement
    agids: str = None # advertisement_group
    cnids: str = None # company_name

    # Created by us
    receive_date: str = None  # Raw request receive date
    raw_request_uid: str = None  # raw request uid, defined by us

    appmetrica_device_id: str = None
    appmetrica_profile_id: str = None
    os_name: str = None
    
    # Use for analitics calculated by us
    channel: str = None
    buyer: str = None
