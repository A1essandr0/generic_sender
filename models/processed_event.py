from pydantic import BaseModel


class ProcessedEvent(BaseModel):
    # these are base fields from raw event
    event_id: str = None
    created: str = None
    source: str = None
    payout: str = None

    # these are added by processors
    app_id: str = None

    event_value: str = None
    event_name: str = None
    process_time: str = None
    process_date: str = None


    os_name: str = None
    appmetrica_device_id: str = None
    appmetrica_profile_id: str = None

    instance_id: str = None
    advertising_id: str = None
    af_events_api: str = None

    my_tracker_status: str = None
    my_tracker_rsp: str = None
    appmetrica_status: str = None
    appmetrica_rsp: str = None
    appsflyer_status: str = None
    appsflyer_rsp: str = None

    error: str = None

