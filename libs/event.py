from abc import ABC, abstractmethod

class Event(ABC):
    @abstractmethod
    def __init__(self):
        """"""

    @abstractmethod
    def send(self, data, msg_key, topic, sender_impl, data_fields, metrics, mappings):
        """"""