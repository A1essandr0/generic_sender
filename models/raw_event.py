from pydantic import BaseModel


class RawEvent(BaseModel):
    event_id: str = None
    created: str = None
    source: str = None
    payout: str = None