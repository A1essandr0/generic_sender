import logging
import asyncio
import json

import aiohttp
from aiokafka import AIOKafkaConsumer

from fixtures import (
    requests_fixture as fixture
)
from setup import setUp
from teardown import tearDown

import libs.config_loader as config_loader
import libs.logger_colorer as colorer


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colorer.colored_stream,]
)
logger = logging.getLogger(__name__)
basic_url = "0.0.0.0:8000"


async def test_collector():
    passed_consumer = AIOKafkaConsumer(
        config.get(config_loader.PASSED_REQUESTS_TOPIC),
        bootstrap_servers=config.get(config_loader.KAFKA_BROKER),
        group_id="test-group-passed"
    )
    filtered_consumer = AIOKafkaConsumer(
        config.get(config_loader.FILTERED_REQUESTS_TOPIC),
        bootstrap_servers=config.get(config_loader.KAFKA_BROKER),
        group_id="test-group-filtered"
    )
    await passed_consumer.start(), await filtered_consumer.start()

    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"http://{basic_url}{fixture.request_string_1}") as response:
            assert response.status == 200
        async with session.get(url=f"http://{basic_url}{fixture.request_string_2}") as response:
            assert response.status == 200

    passed_message, filtered_message = await asyncio.gather(
        passed_consumer.getone(), filtered_consumer.getone()
    )
    assert json.loads(passed_message.value.decode("UTF-8")
        )["adids"] == "ekapusta"
    assert json.loads(filtered_message.value.decode("UTF-8")
        )["adids"] == "RAZDVATRI"

    await passed_consumer.stop(), await filtered_consumer.stop()
    logger.warning(f"ran test_collector_and_filter okay")


async def test_sender():
    processed_consumer = AIOKafkaConsumer(
        config.get(config_loader.PROCESSED_REQUESTS_TOPIC),
        bootstrap_servers=config.get(config_loader.KAFKA_BROKER),
        group_id="test-group-processed-appsflyer"
    )
    await processed_consumer.start()

    processed_message = await processed_consumer.getone()
    app_id, appsflyer_response, appsflyer_status = json.loads(processed_message.value.decode("UTF-8")
        )["app_id"], json.loads(processed_message.value.decode("UTF-8")
        )["appsflyer_rsp"], json.loads(processed_message.value.decode("UTF-8")
        )["appsflyer_status"]

    assert app_id == "58479"
    print(processed_message)

    await processed_consumer.stop()
    logger.warning(f"ran appsflyer_sender okay, response: {appsflyer_response}, status: {appsflyer_status}")




async def run_all():
    await setUp()

    await test_collector()

    await test_sender()

    await tearDown()


asyncio.run(
    run_all()
)
