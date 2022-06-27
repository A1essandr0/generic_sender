import asyncio

import faust

from pydantic_serializer import PydanticSerializer
import libs.config_loader as config_loader

from models.raw_event import RawEvent
from models.processed_event import ProcessedEvent

from libs.sender import Sender
import processors
import event_senders
import sender_impl
from mappings import mappings_dict

config = config_loader.Config()


app = faust.App(
    f"{config_loader.SERVICE_NAME}-0",
    broker=config.get(config_loader.KAFKA_BROKER),
    web_host=config.get(config_loader.WEB_HOST),
    web_port=config.get(config_loader.WEB_PORT),    
)

raw_events_topic = app.topic(
    config.get(config_loader.RAW_EVENTS_TOPIC), partitions=8, value_serializer=PydanticSerializer(RawEvent)
)
processed_events_topic = app.topic(
    config.get(config_loader.PROCESSED_EVENTS_TOPIC), partitions=8, value_serializer=PydanticSerializer(ProcessedEvent)
)


mytracker_sender = Sender(
    sender_implementation=sender_impl.mock_send_event_mytracker, # implementation of sending event to outer system
    topic=processed_events_topic,
    data_fields={"status": "my_tracker_status", "response": "my_tracker_rsp"},
    metrics={"instance_name": "mock_mytracker_sender"},
    mappings_dict=mappings_dict, # mappings are data used in processing
)
mytracker_sender.register_processors([
    processors.mock_processor,
    processors.make_conversion,
    processors.add_app_id,
    processors.add_os_parameter
])
mytracker_sender.register_event_senders([
    event_senders.mock_event_sender,
    event_senders.process_filled_out_form_event,
])
asyncio.ensure_future(mytracker_sender.initialize_mappings())


appsflyer_sender = Sender(
    sender_implementation=sender_impl.mock_send_event_appsflyer,
    topic=processed_events_topic,
    data_fields={"status": "appsflyer_status", "response": "appsflyer_rsp"},
    metrics={"instance_name": "mock_appsflyer_sender"},
    mappings_dict=mappings_dict,
)
appsflyer_sender.register_processors([
    processors.mock_processor,
    processors.make_conversion,
    processors.add_app_id,
    processors.add_os_parameter
])
appsflyer_sender.register_event_senders([
    event_senders.mock_event_sender,
    event_senders.process_filled_out_form_event,
])
asyncio.ensure_future(appsflyer_sender.initialize_mappings())


appmetrica_sender = Sender(
    sender_implementation=sender_impl.mock_send_event_appmetrica,
    topic=processed_events_topic,
    data_fields={"status": "appmetrica_status", "response": "appmetrica_rsp"},
    metrics={"instance_name": "mock_appmetrica_sender"},
    mappings_dict=mappings_dict,
)
appmetrica_sender.register_processors([
    processors.mock_processor,
    processors.make_conversion,
    processors.add_app_id,
    processors.add_os_parameter
])
appmetrica_sender.register_event_senders([
    event_senders.mock_event_sender,
    event_senders.process_filled_out_form_event,
])
asyncio.ensure_future(appmetrica_sender.initialize_mappings())


initialized_senders = (
    mytracker_sender, 
    appsflyer_sender, 
    appmetrica_sender,
)