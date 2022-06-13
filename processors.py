import datetime, time

import libs.constants as constants
from models.conversion import Conversion


async def make_conversion(data, mappings):
    conv = Conversion(**data.dict())
    conv.instance_id = data.aff_sub1
    conv.advertising_id = ""
    conv.af_events_api = "true"
    conv.event_value = ""
    conv.process_date = datetime.datetime.utcnow().isoformat()
    conv.process_time = int(time.time())
    return conv

async def add_app_id(data, mappings):
    app_id = mappings[constants.CONFIG_KEY_APP_MAPPING].get(data.source, None)
    data.app_id = app_id
    return data

async def add_appmetrica_profile_id(data, mappings):
    aff_sub1_split = data.aff_sub1.split("_")
    if len(aff_sub1_split) == 2:
        data.appmetrica_profile_id = aff_sub1_split[1]
    return data