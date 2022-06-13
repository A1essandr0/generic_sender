import aioredis
import logging
import json

from libs.constants import mappings, default_values
from libs.logger_colorer import colored_stream
from libs.singleton import MetaSingleton
import libs.config_loader as config_loader


config = config_loader.Config()
logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)), 
    format=config.get(config_loader.LOGGING_FORMAT),
    handlers=[colored_stream,]
)
logger = logging.getLogger(__name__)


class ConfigStore(metaclass=MetaSingleton):
    def __init__(self):
        logger.info(
            "Configure redis client: {}:{}".format(
                config.get(config_loader.KEYDB_HOST), 
                config.get(config_loader.KEYDB_PORT)
            )
        )
        self.db = aioredis.Redis(
            host=config.get(config_loader.KEYDB_HOST),
            port=config.get(config_loader.KEYDB_PORT),
            db=config.get(config_loader.KEYDB_DB_NUM),
            password=config.get(config_loader.KEYDB_PASS),
        )

    async def get_mapping(self, mapping_name: str) -> str:
        logger.info(f"Getting {mapping_name}")
        mapping_exists_in_db = await self.db.exists(mappings[mapping_name])
        if not mapping_exists_in_db:
            return default_values[mapping_name]

        mapping_value = await self.db.get(mappings[mapping_name])
        return json.loads(mapping_value)


    async def get_allowed_sources_list(self):
        return await self.get_mapping("allowed_sources_list")

    async def get_app_mapping(self):
        return await self.get_mapping("app_mapping")

    async def get_no_android_id_list(self):
        return await self.get_mapping("no_android_id_list")

    async def get_ios_apps(self):
        return await self.get_mapping("ios_apps")

    async def get_unique_loan_id_list(self):
        return await self.get_mapping("unique_loan_id_list")

    async def get_app_s2s_keys_mapping(self):
        return await self.get_mapping("app_s2s_keys_mapping")

    async def get_appmetrica_app_mapping(self):
        return await self.get_mapping("appmetrica_app_mapping")

    async def get_appmetrica_app_api_key_mapping(self):
        return await self.get_mapping("appmetrica_app_api_key_mapping")

    async def get_appmetrica_profile_id_apps(self):
        return await self.get_mapping("appmetrica_profile_id_apps")
        
    async def get_appsflyer_app_id_mapping(self):
        return await self.get_mapping("appsflyer_app_id_mapping")

    async def get_appsflyer_id_mapping(self):
        return await self.get_mapping("appsflyer_id_mapping")

    async def get_appsflyer_dev_key_mapping(self):
        return await self.get_mapping("appsflyer_dev_key_mapping")
