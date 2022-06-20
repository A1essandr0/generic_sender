import datetime, time

import libs.constants as constants
from models.processed_event import ProcessedEvent


async def mock_processor(data, mappings):
    return data


async def make_conversion(data, mappings):
    processed_event = ProcessedEvent(**data.dict())
    processed_event.event_value = ""
    processed_event.os_name = ""
    processed_event.process_date = datetime.datetime.utcnow().isoformat()
    processed_event.process_time = int(time.time())
    
    return processed_event


async def add_app_id(data, mappings):
    app_id = mappings[constants.CONFIG_KEY_APP_MAPPING].get(data.source, None)
    data.app_id = app_id
    return data


async def add_os_parameter(data, mappings):
    android_applications, ios_applications = (
        mappings[constants.CONFIG_KEY_NO_ANDROID_ID],
        mappings[constants.CONFIG_KEY_IOS_APPS],
    )
    if data.source in android_applications:
        data.os_name = constants.ANDROID_OS_NAME
    elif data.source in ios_applications:
        data.os_name = constants.IOS_OS_NAME

    return data