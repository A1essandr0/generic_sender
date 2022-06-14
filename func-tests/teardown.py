import asyncio
import logging

from fixtures import mappings_values
from setup import delete_keydb_record

import libs.config_loader as config_loader
import libs.logger_colorer as colorer


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colorer.colored_stream,]
)
logger = logging.getLogger(__name__)


async def clear_keydb_store():
    await asyncio.gather(
        *[delete_keydb_record(key) for key in mappings_values.mappings]
    )


async def tearDown():
    await clear_keydb_store()
    logger.warning(f"ran teardown okay")


if __name__ == "__main__":
    asyncio.run(
        tearDown()
    )
