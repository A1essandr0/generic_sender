import logging

from prometheus_client import start_http_server

import libs.config_loader as config_loader
from libs.logger_colorer import colored_stream
import libs.metrics as counters

from faust_application import (
    app, 
    initialized_senders,
    raw_events_topic
)


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colored_stream,]
)
logger = logging.getLogger(__name__)


@app.task
async def on_started() -> None:
    logger.info("Starting prometheus server")
    start_http_server(port=config.get(config_loader.PROMETHEUS_PORT))


@app.agent(raw_events_topic)
async def on_event(stream) -> None:
    async for msg_key, raw_event in stream.items():
        for sender_instance in initialized_senders:
            counters.RAW_EVENTS_READ_CNTR.labels(sender_instance.metrics["instance_name"]).inc()

            processed_event = await sender_instance.process(raw_event)

            if not processed_event.app_id:
                logger.error(f"Unknown source for {sender_instance.metrics['instance_name']}: {processed_event.source}")
                logger.error(F"All params: {processed_event.dict()}")
                counters.UNKNOWN_SOURCE_CNTR.labels(sender_instance.metrics["instance_name"]).inc()

            await sender_instance.send_events(
                processed_event,
                msg_key=msg_key
            )

