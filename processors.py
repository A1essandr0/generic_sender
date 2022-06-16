import datetime, time

import libs.constants as constants
from models.processed_event import ProcessedEvent


async def mock_processor(data, mappings):
    return data


async def make_conversion(data, mappings):
    processed_event = ProcessedEvent(**data.dict())
    processed_event.event_value = ""
    processed_event.process_date = datetime.datetime.utcnow().isoformat()
    processed_event.process_time = int(time.time())
    
    # processed_event.instance_id = data.aff_sub1
    # processed_event.advertising_id = ""
    # processed_event.af_events_api = "true"

    return processed_event


async def add_app_id(data, mappings):
    app_id = mappings[constants.CONFIG_KEY_APP_MAPPING].get(data.source, None)
    data.app_id = app_id
    return data


async def add_appmetrica_profile_id(data, mappings):
    aff_sub1_split = data.aff_sub1.split("_")
    if len(aff_sub1_split) == 2:
        data.appmetrica_profile_id = aff_sub1_split[1]
    return data