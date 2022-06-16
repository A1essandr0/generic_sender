import logging
import asyncio

import faust
from prometheus_client import start_http_server

from pydantic_serializer import PydanticSerializer
import libs.config_loader as config_loader
from libs.logger_colorer import colored_stream
from models.raw_event import RawEvent
from models.processed_event import ProcessedEvent

from libs.sender import Sender
import libs.metrics as counters
import processors
import event_senders
import sender_impl
from mappings import mappings_dict


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colored_stream,]
)
logger = logging.getLogger(__name__)


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


sender = Sender(
    sender_implementation=sender_impl.mock_send_event, # implementation of sending event to outer system
    topic=processed_events_topic,
    data_fields={"status": "generic_status", "response": "generic_rsp"},
    metrics={"instance_name": "generic_sender"},
    mappings_dict=mappings_dict, # mappings are data used in processing
)

sender.register_processors([
    processors.mock_processor,
    processors.make_conversion,
    processors.add_app_id,
])

sender.register_event_senders([
    event_senders.mock_event_sender,
    event_senders.process_filled_out_form_event,
    # event_senders.process_approved_event,
    # event_senders.process_unique_event,
    # event_senders.process_unique_loan_event,
])

asyncio.ensure_future(sender.initialize_mappings())


@app.task
async def on_started() -> None:
    logger.info("Starting prometheus server")
    start_http_server(port=config.get(config_loader.PROMETHEUS_PORT))


@app.agent(raw_events_topic)
async def on_event(stream) -> None:
    async for msg_key, raw_event in stream.items():
        counters.RAW_EVENTS_READ_CNTR.labels(sender.metrics["instance_name"]).inc()

        processed_event = await sender.process(raw_event)

        if not processed_event.app_id:
            logger.error(f"Unknown source: {processed_event.source}")
            logger.error(F"All params: {processed_event.dict()}")
            counters.UNKNOWN_SOURCE_CNTR.labels(sender.metrics["instance_name"]).inc()
            yield processed_event
        
        await sender.send_events(
            processed_event, 
            msg_key=msg_key
        )

        yield processed_event