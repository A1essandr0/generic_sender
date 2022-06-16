import logging

import models.constants
import libs.metrics as counters
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


# function-based events
async def mock_event_sender(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    pass


async def process_filled_out_form_event(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    data.event_name = models.constants.EVENT_NAME_FILLED_OUT_FORM
    app_type = "android" if data.app_id not in mappings[constants.CONFIG_KEY_IOS_APPS] else "ios"

    status_value, response_value = await sender_impl(data, mappings, metrics)

    if status_value == 200:
        if app_type == "android":
            counters.FILLED_OUT_FORM_EVENTS_ANDROID_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
        elif app_type == "ios":
            counters.FILLED_OUT_FORM_EVENTS_IOS_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
    else:
        if app_type == "android":
            counters.FILLED_OUT_FORM_EVENTS_ANDROID_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()
        elif app_type == "ios":
            counters.FILLED_OUT_FORM_EVENTS_IOS_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()

    if data_fields and "status" in data_fields:
        setattr(data, data_fields["status"], status_value)
    if data_fields and "response" in data_fields:
        setattr(data, data_fields["response"], response_value)

    logger.info(f"sending filled out form event to topic: {data}")
    await topic.send(key=msg_key, value=data)


async def process_status_based_event(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    logger.warn(f"Status-based event: {data.event_name=} {data.status=}")



async def process_approved_event(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    if data.status == models.constants.EVENT_STATUS_APPROVED:
        data.event_name = models.constants.EVENT_NAME_APPROVED
        app_type = "android" if data.app_id not in mappings[constants.CONFIG_KEY_IOS_APPS] else "ios"

        status_value, response_value = await sender_impl(data, mappings, metrics)

        if status_value == 200:
            if app_type == "android":
                counters.APPROVED_ANDROID_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
            elif app_type == "ios":
                counters.APPROVED_IOS_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
        else:
            if app_type == "android":
                counters.APPROVED_ANDROID_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()
            elif app_type == "ios":
                counters.APPROVED_IOS_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()

        if data_fields and "status" in data_fields:
            setattr(data, data_fields["status"], status_value)
        if data_fields and "response" in data_fields:
            setattr(data, data_fields["response"], response_value)
        
        logger.info(f"sending approved event to topic: {data}")
        await topic.send(key=msg_key, value=data)


async def process_unique_event(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    if (data.status == models.constants.EVENT_STATUS_APPROVED
            or data.status == models.constants.EVENT_STATUS_PENDING):
        data.event_name = models.constants.EVENT_NAME_UNIQUE_EVENT
        app_type = "android" if data.app_id not in mappings[constants.CONFIG_KEY_IOS_APPS] else "ios"

        status_value, response_value = await sender_impl(data, mappings, metrics)

        if status_value == 200:
            if app_type == "android":
                counters.UNIQUE_ANDROID_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
            elif app_type == "ios":
                counters.UNIQUE_IOS_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
        else:
            if app_type == "android":
                counters.UNIQUE_ANDROID_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()
            elif app_type == "ios":
                counters.UNIQUE_IOS_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()

        if data_fields and "status" in data_fields:
            setattr(data, data_fields["status"], status_value)
        if data_fields and "response" in data_fields:
            setattr(data, data_fields["response"], response_value)
        
        logger.info(f"sending unique event to topic: {data}")
        await topic.send(key=msg_key, value=data)


async def process_unique_loan_event(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    if (data.partner and data.type_event
            and data.partner.lower() in config.get(config_loader.UNIQUE_LOAN_PARTNERS)
            and data.type_event.lower() == "new"
            and data.offer_id
            and int(data.offer_id) in mappings["unique_loan_id_list"]):
        data.event_name = models.constants.EVENT_NAME_UNIQUE_LOAN
        app_type = "android" if data.app_id not in mappings[constants.CONFIG_KEY_IOS_APPS] else "ios"

        status_value, response_value = await sender_impl(data, mappings, metrics)

        if status_value == 200:
            if app_type == "android":
                counters.UNIQUE_LOAN_ANDROID_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
            elif app_type == "ios":
                counters.UNIQUE_LOAN_IOS_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
        else:
            if app_type == "android":
                counters.UNIQUE_LOAN_ANDROID_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()
            elif app_type == "ios":
                counters.UNIQUE_LOAN_IOS_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()

        if data_fields and "status" in data_fields:
            setattr(data, data_fields["status"], status_value)
        if data_fields and "response" in data_fields:
            setattr(data, data_fields["response"], response_value)
        
        logger.info(f"sending unique loan event to topic: {data}")
        await topic.send(key=msg_key, value=data)
