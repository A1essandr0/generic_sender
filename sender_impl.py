import json
import aiohttp
import logging
from urllib.parse import urlencode

import libs.constants as constants
import libs.config_loader as config_loader
from libs.logger_colorer import colored_stream


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colored_stream,]
)
logger = logging.getLogger(__name__)


async def mock_send_event_mytracker(data, mappings, metrics):
    logger.info(f"Mytracker sender sends its regards")
    return 200, "OK"

async def mock_send_event_appsflyer(data, mappings, metrics):
    logger.info(f"Appsflyer sender sends its regards")
    return 200, "OK"

async def mock_send_event_appmetrica(data, mappings, metrics):
    logger.info(f"Appmetrica sender its regards")
    return 200, "OK"


async def send_event_appmetrica(data, mappings, metrics):
    appmetrica_app_id = mappings[constants.CONFIG_KEY_APPMETRICA_APP_MAPPING].get(data.source, None)
    app_api_key = mappings[constants.CONFIG_KEY_APPMETRICA_APP_API_KEY_MAPPING].get(data.source, None)

    base_url = f"{config.get(config_loader.APPMETRICA_URL)}"
    parameters = {
        "post_api_key": app_api_key,
        "application_id": appmetrica_app_id,
        "event_timestamp": data.process_time,
        "event_name": data.event_name,
    }

    if data.appmetrica_device_id:
        logger.info(f"Set appmetrica_device_id to parameters: {data.appmetrica_device_id}")
        parameters["appmetrica_device_id"] = data.appmetrica_device_id

    if data.appmetrica_profile_id and not data.appmetrica_device_id:
        logger.info(f"Set profile_id to parameters: {data.appmetrica_profile_id}")
        parameters["profile_id"] = data.appmetrica_profile_id

    encoded_parameters = urlencode(parameters)
    logger.info(f"Encoded params: {encoded_parameters}")

    async with aiohttp.ClientSession() as session:
        async with session.post(base_url, params=encoded_parameters) as response:
            response_text = await response.text()

            logger.info(f"Source: {data.app_id} Appmetrica status code: {response.status} response: {response_text}")
            if response.status != 200:
                logger.error(
                    f"Source: {data.app_id} Could not send appmetrica event. Returned code: {response.status}, returned message: {response_text}"
                )

            return response.status, response_text



async def send_event_mytracker(data, mappings, metrics):
    app_type = "android" if data.app_id not in mappings[constants.CONFIG_KEY_IOS_APPS] else "ios"
    transformed_data = {}

    if app_type == "android":
        if data.aff_sub5 and data.aff_sub5.lower() not in ["not_granted", "unknown"]:
            transformed_data["gaid"] = data.aff_sub5
        if data.aff_sub4:
            transformed_data["androidId"] = data.aff_sub4 if data.source not in mappings["no_android_id_list"] else None
    elif app_type == "ios":
        if data.aff_sub5:
            transformed_data["idfa"] = data.aff_sub5
        if data.aff_sub4:
            transformed_data["iosVendorId"] = data.aff_sub4

    if data.event_name:
        transformed_data["customEventName"] = data.event_name
    if data.process_time:
        transformed_data["eventTimestamp"] = data.process_time
    if data.instance_id:
        transformed_data["instanceId"] = data.instance_id.split('_')[0]
    # if data.custom_event_params:
    #     transformed_data["customEventParams"] = data.custom_event_params

    headers = {
        "Authorization": mappings[constants.CONFIG_KEY_S2S_KEYS_MAPPING].get(data.app_id, config.get(config_loader.DEFAULT_S2S_KEY)),
        "content-type": "application/json",
    }
    mytracker_url = f"{config.get(config_loader.MYTRACKER_URL)}?idApp={data.app_id}"

    logger.info(f"Sending data: {transformed_data} to mytracker")
    async with aiohttp.ClientSession() as session:
        async with session.post(mytracker_url, data=json.dumps(transformed_data), headers=headers) as response:
            response_text = await response.text()
            logger.info(f"Source: {data.source} Mytracker status code: {response.status} response: {response_text}")

            if response.status != 200:
                logger.error(f"Source: {data.source} Could not to send mytracker event: {response_text}")

            return response.status, response_text



async def send_event_appsflyer(data, mappings, metrics):
    transformed_data = {
        "appsflyer_id": mappings[constants.CONFIG_KEY_APPSFLYER_ID_MAPPING].get(
            data.source, ""
        ),
        "eventName": data.event_name,
        "eventValue": data.event_value,
    }
    if data.process_time:
        transformed_data["eventTime"] = data.process_time

    app_type = "android" if data.app_id not in mappings[constants.CONFIG_KEY_IOS_APPS] else "ios"
    if app_type == "android":
        if data.aff_sub5 and data.aff_sub5.lower() not in ["not_granted", "unknown"]:
            transformed_data["advertising_id"] = data.aff_sub5
        if data.aff_sub4:
            transformed_data["androidId"] = data.aff_sub4 if data.source not in mappings["no_android_id_list"] else None
    elif app_type == "ios":
        if data.aff_sub5:
            transformed_data["idfa"] = data.aff_sub5
        if data.aff_sub4:
            transformed_data["iosVendorId"] = data.aff_sub4

    headers = {
        "authentication": mappings[constants.CONFIG_KEY_APPSFLYER_DEV_KEY_MAPPING].get(
            data.source, ""
        ),
        "content-type": "application/json",
    }

    app_url = mappings[constants.CONFIG_KEY_APPSFLYER_APP_MAPPING].get(
        data.source, ""
    )
    if app_type == "ios":
        app_url = f"id{app_url}"
    url = f"{config.get(config_loader.APPSFLYER_URL)}/{app_url}"


    logger.warn(f"To send: {headers} {url} {transformed_data}")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(transformed_data), headers=headers) as response:
            response_text = await response.text()

            logger.info(f"Source: {data.source} Appsflyer status code: {response.status} response: {response_text}")
            if response.status != 200:
                logger.error(
                    f"Source: {data.source} Could not send appsflyer event. Returned code: {response.status}, returned message: {response_text}"
                )

            return response.status, response_text