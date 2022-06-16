import os

from libs.singleton import MetaSingleton
from configloader import ConfigLoader

config_abs_path = "/".join(os.path.abspath(__file__).split("/")[0:-2])
SERVICE_NAME = "GENERIC_SENDER"
ENV_CONFIG_PATH = os.getenv(f"{SERVICE_NAME}_CONFIG_PATH")


class Config(metaclass=MetaSingleton):
    def __init__(self, config_file_path=os.path.join(config_abs_path, "config.yml")):
        self.config_loader = ConfigLoader()
        if ENV_CONFIG_PATH:
            print(f"Use config file from env: {ENV_CONFIG_PATH}")
            self.config_loader.update_from_yaml_file(ENV_CONFIG_PATH)
        else:
            print(f"Use default config file: {config_file_path}")
            self.config_loader.update_from_yaml_file(config_file_path)
        self.config_loader.update_from_env_namespace(f"{SERVICE_NAME}")
        print(self.to_dict())

    def get(self, setting_name):
        return self.config_loader.get(setting_name, None)

    def to_dict(self):
        loader = self.config_loader
        return {key: loader.get(key) for key in loader.keys()}


LOGGING_LEVEL = "LOGGING_LEVEL"
LOGGING_FORMAT = "LOGGING_FORMAT"

WEB_HOST = "WEB_HOST"
WEB_PORT = "WEB_PORT"
PROMETHEUS_PORT = "PROMETHEUS_PORT"
KAFKA_BROKER = "KAFKA_BROKER"

RAW_EVENTS_TOPIC = "RAW_EVENTS_TOPIC"
PROCESSED_EVENTS_TOPIC = "PROCESSED_EVENTS_TOPIC"

KEYDB_HOST = "KEYDB_HOST"
KEYDB_PORT = "KEYDB_PORT"
KEYDB_DB_NUM = "KEYDB_DB_NUM"
KEYDB_PASS = "KEYDB_PASS"


DEFAULT_S2S_KEY = "DEFAULT_S2S_KEY"

MYTRACKER_URL = "MYTRACKER_URL"
APPMETRICA_URL = "APPMETRICA_URL"
APPSFLYER_URL = "APPSFLYER_URL"

APPMETRICA_APP_API_KEY_MAPPING = "APPMETRICA_APP_API_KEY_MAPPING"


UNIQUE_LOAN_PARTNERS = "UNIQUE_LOAN_PARTNERS"