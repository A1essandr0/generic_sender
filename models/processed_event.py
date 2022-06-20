from pydantic import BaseModel


class ProcessedEvent(BaseModel):
    # these are base fields from raw event
    source: str = None
    event_name: str = None
    event_status: str = None
    created: str = None
    payout: str = None

    # these are added by processors
    app_id: str = None

    event_value: str = None
    process_time: str = None
    process_date: str = None
    os_name: str = None

    my_tracker_status: str = None
    my_tracker_rsp: str = None
    appmetrica_status: str = None
    appmetrica_rsp: str = None
    appsflyer_status: str = None
    appsflyer_rsp: str = None

    error: str = None

