import asyncio
import logging
import json

import aioredis

from fixtures import (
    mappings_values,
)
import libs.config_loader as config_loader
import libs.logger_colorer as colorer


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colorer.colored_stream,]
)
logger = logging.getLogger(__name__)

keydb_client = aioredis.Redis(
    host=config.get(config_loader.KEYDB_HOST),
    port=config.get(config_loader.KEYDB_PORT),
    db=config.get(config_loader.KEYDB_DB_NUM),
    password=config.get(config_loader.KEYDB_PASS)
)


async def get_keydb_value(key: str) -> str:   
    value = await keydb_client.get(key)
    return value

async def set_keydb_value(key: str, value: str) -> bool:
    await keydb_client.set(key, value)
    return True

async def delete_keydb_record(key: str) -> bool:
    await keydb_client.delete(key)
    return True


async def set_up_keydb_store():
    await asyncio.gather(
        *[set_keydb_value(key, json.dumps(value))
            for key, value in mappings_values.mappings.items()]
    )


async def setUp():
    await set_up_keydb_store()
    logger.warning(f"ran setup okay")


if __name__ == "__main__":
    asyncio.run(
        setUp()
    )

