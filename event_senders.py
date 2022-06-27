import logging

import models.constants
import libs.metrics as counters
import libs.constants as constants
import libs.config_loader as config_loader
from libs.logger_colorer import colored_stream

from libs.event import Event


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colored_stream,]
)
logger = logging.getLogger(__name__)


# function-based events
async def mock_event_sender(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    status_value, response_value = await sender_impl(data, mappings, metrics)

    if data_fields and "status" in data_fields:
        setattr(data, data_fields["status"], status_value)
    if data_fields and "response" in data_fields:
        setattr(data, data_fields["response"], response_value)

    logger.warn(f"MOCK sending event: {data=} to {topic=}")
    await topic.send(key=msg_key, value=data)


async def process_filled_out_form_event(data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
    if data.event_name == models.constants.EVENT_NAME_FILLED_OUT_FORM:
        status_value, response_value = await sender_impl(data, mappings, metrics)

        if status_value == 200:
            if data.os_name == constants.ANDROID_OS_NAME:
                counters.FILLED_OUT_FORM_EVENTS_ANDROID_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
            elif data.os_name == constants.IOS_OS_NAME:
                counters.FILLED_OUT_FORM_EVENTS_IOS_SENT_SUCCESSFULLY_CNTR.labels(metrics["instance_name"]).inc()
        else:
            if data.os_name == constants.ANDROID_OS_NAME:
                counters.FILLED_OUT_FORM_EVENTS_ANDROID_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()
            if data.os_name == constants.IOS_OS_NAME:
                counters.FILLED_OUT_FORM_EVENTS_IOS_SENT_FAILED_CNTR.labels(metrics["instance_name"]).inc()

        if data_fields and "status" in data_fields:
            setattr(data, data_fields["status"], status_value)
        if data_fields and "response" in data_fields:
            setattr(data, data_fields["response"], response_value)

        logger.info(f"Sending {data.event_name=} {data=} to topic {topic=}")
        await topic.send(key=msg_key, value=data)


# class-based events
class MockEvent(Event):
    pass