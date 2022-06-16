import logging

from libs.singleton import MetaSingleton

logger = logging.getLogger(__name__)


class InmemoryDB(metaclass=MetaSingleton):
    def __init__(self):
        self.db = {}

    def all(self):
        return self.db

    def clear(self):
        self.db.clear()

    def put(self, key: str, value: int):
        self.db[key] = value

    def get(self, key: str):
        return self.db.get(key, None)

    def delete(self, key):
        print("Key: ", key)
        del self.db[key]

    def __iter__(self):
        return self

    def __next__(self):
        for k in self.db:
            yield k


class MetricsStore:
    def __init__(self):
        logger.info("Init metrics store")
        self.db = InmemoryDB()

    def clear_all_metrics(self):
        logger.info("Clear all keys in metrics store")
        self.db.clear()

    def get_all_metrics(self):
        logger.info("Get all metrics from store")
        return self.db.all()

    def get_metric_value(self, metric_name: str) -> int:
        logger.info(f"Get value for metric: {metric_name}")
        value = self.db.get(metric_name)
        logger.info(f"Got value: {value}")
        return value if value else 0

    def set_metric_value(self, metric_name: str, value: int) -> int:
        logger.info(f"Set value: {value} for metric: {metric_name}")
        self.db.put(metric_name, value)

    def inc(self, metric_name: str, inc_value: int = 1):
        logger.info(f"Increment value for metric: {metric_name}")
        value = self.get_metric_value(metric_name)
        value += inc_value
        logger.info(f"New value: {value} for metric: {metric_name}")
        self.set_metric_value(metric_name, value)
