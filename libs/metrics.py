from prometheus_client import Counter

RAW_EVENTS_READ_CNTR = Counter("RAW_EVENTS_READ_CNTR", "Number of raw events read from kafka", ["sender_instance",])
UNKNOWN_SOURCE_CNTR = Counter("UNKNOWN_SOURCE_CNTR", "Number raw requests with unknown source", ["sender_instance",])

FILLED_OUT_FORM_EVENTS_ANDROID_SENT_SUCCESSFULLY_CNTR = Counter("FILLED_OUT_FORM_EVENTS_ANDROID_SENT_SUCCESSFULLY_CNTR", "Number of filled out form android events sent", ["sender_instance",])
FILLED_OUT_FORM_EVENTS_ANDROID_SENT_FAILED_CNTR = Counter("FILLED_OUT_FORM_EVENTS_ANDROID_SENT_FAILED_CNTR", "Number of filled out form android events sending failed", ["sender_instance",])
FILLED_OUT_FORM_EVENTS_IOS_SENT_SUCCESSFULLY_CNTR = Counter("FILLED_OUT_FORM_EVENTS_IOS_SENT_SUCCESSFULLY_CNTR", "Number of filled out form ios events sent", ["sender_instance",])
FILLED_OUT_FORM_EVENTS_IOS_SENT_FAILED_CNTR = Counter("FILLED_OUT_FORM_EVENTS_IOS_SENT_FAILED_CNTR", "Number of filled out form ios events sending failed", ["sender_instance",])



APPROVED_ANDROID_SENT_SUCCESSFULLY_CNTR = Counter("APPROVED_ANDROID_SENT_SUCCESSFULLY_CNTR", "Number of approved android events sent", ["sender_instance",])
APPROVED_ANDROID_SENT_FAILED_CNTR = Counter("APPROVED_ANDROID_SENT_FAILED_CNTR", "Number of approved android events sending failed", ["sender_instance",])
APPROVED_IOS_SENT_SUCCESSFULLY_CNTR = Counter("APPROVED_IOS_SENT_SUCCESSFULLY_CNTR", "Number of approved ios events sent", ["sender_instance",])
APPROVED_IOS_SENT_FAILED_CNTR = Counter("APPROVED_IOS_SENT_FAILED_CNTR", "Number of approved ios events sending failed", ["sender_instance",])

UNIQUE_ANDROID_SENT_SUCCESSFULLY_CNTR = Counter("UNIQUE_ANDROID_SENT_SUCCESSFULLY_CNTR", "Number of unique android events sent", ["sender_instance",])
UNIQUE_ANDROID_SENT_FAILED_CNTR = Counter("UNIQUE_ANDROID_SENT_FAILED_CNTR", "Number of unique android events sending failed", ["sender_instance",])
UNIQUE_IOS_SENT_SUCCESSFULLY_CNTR = Counter("UNIQUE_IOS_SENT_SUCCESSFULLY_CNTR", "Number of unique ios events sent", ["sender_instance",])
UNIQUE_IOS_SENT_FAILED_CNTR = Counter("UNIQUE_IOS_SENT_FAILED_CNTR", "Number of unique ios events sending failed", ["sender_instance",])

UNIQUE_LOAN_ANDROID_SENT_SUCCESSFULLY_CNTR = Counter("UNIQUE_LOAN_ANDROID_SENT_SUCCESSFULLY_CNTR", "Number of unique loan android events sent", ["sender_instance",])
UNIQUE_LOAN_ANDROID_SENT_FAILED_CNTR = Counter("UNIQUE_LOAN_ANDROID_SENT_FAILED_CNTR", "Number of unique loan android events sending failed", ["sender_instance",])
UNIQUE_LOAN_IOS_SENT_SUCCESSFULLY_CNTR = Counter("UNIQUE_LOAN_IOS_SENT_SUCCESSFULLY_CNTR", "Number of unique loan ios events sent", ["sender_instance",])
UNIQUE_LOAN_IOS_SENT_FAILED_CNTR = Counter("UNIQUE_LOAN_IOS_SENT_FAILED_CNTR", "Number of unique loan ios events sending failed", ["sender_instance",])