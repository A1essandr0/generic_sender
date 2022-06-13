from pydantic import BaseModel


class Conversion(BaseModel):
    # From raw request
    conversion_id: int = None
    created: str = None
    offer_id: int = None
    source: str = None
    aff_sub1: str = None
    aff_sub2: str = None
    aff_sub3: str = None
    aff_sub4: str = None
    aff_sub5: str = None
    aff_sub6: str = None
    status: str = None
    sum: str = None
    partner: str = None
    type_event: str = None
    payout: str = None
    currency: str = None

    adids: str = None
    agids: str = None
    cnids: str = None

    raw_request_uid: str = None  # raw request uid, defined by us
    # Raw request receive date
    receive_date: str = None
    app_id: str = None

    os_name: str = None
    appmetrica_device_id: str = None
    appmetrica_profile_id: str = None

    instance_id: str = None
    event_name: str = None
    advertising_id: str = None
    af_events_api: str = None
    event_value: str = None

    conversions_id: str = None

    my_tracker_status: str = None
    my_tracker_rsp: str = None
    appmetrica_status: str = None
    appmetrica_rsp: str = None
    appsflyer_status: str = None
    appsflyer_rsp: str = None

    # The same value, but process_time is timestamp process_date iso datetime str
    process_time: str = None
    process_date: str = None

    error: str = None

