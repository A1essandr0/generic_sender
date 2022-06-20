from pydantic import BaseModel


class RawEvent(BaseModel):
    source: str = None
    event_name: str = None
    event_status: str = None
    created: str = None
    payout: str = None