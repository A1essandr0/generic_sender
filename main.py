import logging
import asyncio

import faust
from prometheus_client import start_http_server

from pydantic_serializer import PydanticSerializer
import libs.config_loader as config_loader
from libs.logger_colorer import colored_stream
from models.raw_request import RawRequest
from models.conversion import Conversion

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


# Data comes from this topic to be processed
passed_requests_topic = app.topic(
    config.get(config_loader.PASSED_REQUESTS_TOPIC), partitions=8, value_serializer=PydanticSerializer(RawRequest)
)
# After processing data goes to this topic
processed_requests_topic = app.topic(
    config.get(config_loader.PROCESSED_REQUESTS_TOPIC), partitions=8, value_serializer=PydanticSerializer(Conversion)
)


sender = Sender(
    # implementation of sending event to outer system
    sender_implementation=sender_impl.send_event_appsflyer,

    topic=processed_requests_topic,

    data_fields={"status": "generic_status", "response": "generic_rsp"},
    metrics={"instance_name": "generic_sender"},

    # mappings are data used in processing
    mappings_dict=mappings_dict,
)

sender.register_processors([
    processors.make_conversion,
    processors.add_app_id,
])

sender.register_event_senders([
    event_senders.process_filled_out_form_event,
    event_senders.process_approved_event,
    event_senders.process_unique_event,
    event_senders.process_unique_loan_event,
])

asyncio.ensure_future(sender.initialize_mappings())


@app.task
async def on_started() -> None:
    logger.info("Starting prometheus server")
    start_http_server(port=config.get(config_loader.PROMETHEUS_PORT))


@app.agent(passed_requests_topic)
async def on_event(stream) -> None:
    async for msg_key, raw_request in stream.items():
        counters.RAW_REQUESTS_READ_CNTR.labels(sender.metrics["instance_name"]).inc()

        processed_request = await sender.process(raw_request)
        if not processed_request.app_id:
            logger.error(f"Unknown source: {processed_request.source}")
            logger.error(F"All params: {processed_request.dict()}")
            counters.UNKNOWN_SOURCE_CNTR.labels(sender.metrics["instance_name"]).inc()
            yield processed_request
        
        await sender.send_events(
            processed_request, 
            msg_key=msg_key
        )

        yield processed_request