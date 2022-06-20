from prometheus_client import Counter

RAW_EVENTS_READ_CNTR = Counter("RAW_EVENTS_READ_CNTR", "Number of raw events read from kafka", ["sender_instance",])
UNKNOWN_SOURCE_CNTR = Counter("UNKNOWN_SOURCE_CNTR", "Number raw requests with unknown source", ["sender_instance",])

FILLED_OUT_FORM_EVENTS_ANDROID_SENT_SUCCESSFULLY_CNTR = Counter("FILLED_OUT_FORM_EVENTS_ANDROID_SENT_SUCCESSFULLY_CNTR", "Number of filled out form android events sent", ["sender_instance",])
FILLED_OUT_FORM_EVENTS_ANDROID_SENT_FAILED_CNTR = Counter("FILLED_OUT_FORM_EVENTS_ANDROID_SENT_FAILED_CNTR", "Number of filled out form android events sending failed", ["sender_instance",])
FILLED_OUT_FORM_EVENTS_IOS_SENT_SUCCESSFULLY_CNTR = Counter("FILLED_OUT_FORM_EVENTS_IOS_SENT_SUCCESSFULLY_CNTR", "Number of filled out form ios events sent", ["sender_instance",])
FILLED_OUT_FORM_EVENTS_IOS_SENT_FAILED_CNTR = Counter("FILLED_OUT_FORM_EVENTS_IOS_SENT_FAILED_CNTR", "Number of filled out form ios events sending failed", ["sender_instance",])

