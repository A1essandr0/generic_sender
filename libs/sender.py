import asyncio


class Sender:
    """ Generic sender class """
    def __init__(
        self, 
        sender_implementation=None, 
        topic=None, 
        data_fields=None, 
        metrics=None,
        mappings_dict=None
    ):
        self.processors = []
        self.event_senders = []
        self.sender_implementation = sender_implementation
        self.topic = topic
        self.data_fields = data_fields or {}
        self.metrics = metrics or {}
        self.mappings = mappings_dict or {}


    def register_processors(self, processors):
        self.processors.extend(processors)

    def register_event_senders(self, event_senders):
        self.event_senders.extend(event_senders)


    async def initialize_mappings(self):
        mapping_futures = [self.mappings[key] for key in sorted(self.mappings)]
        if mapping_futures:
            mapping_values = await asyncio.gather(*[future() for future in mapping_futures])
            for key, value in zip(sorted(self.mappings), mapping_values):
                self.mappings[key] = value


    async def process(self, data):
        for processor in self.processors:
            data = await processor(data, self.mappings)
        return data

    async def send_events(self, data, msg_key):
        for event_sender in self.event_senders:
            await event_sender(
                data, 
                msg_key, 
                self.topic, 
                self.sender_implementation, 
                self.data_fields, 
                self.metrics,
                self.mappings
            )
