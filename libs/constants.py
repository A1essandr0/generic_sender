CONFIG_KEY_APP_MAPPING = "app_mapping"
CONFIG_KEY_NO_ANDROID_ID = "no_android_id_list"
CONFIG_KEY_IOS_APPS = "ios_apps"
CONFIG_KEY_UNIQUE_LOAN = "unique_loan_id_list"
CONFIG_KEY_S2S_KEYS_MAPPING = "app_s2s_keys_mapping"
CONFIG_KEY_ALLOWED_SOURCES = "allowed_sources_list"

CONFIG_KEY_APPMETRICA_APP_MAPPING = "appmetrica_app_mapping"
CONFIG_KEY_APPMETRICA_APP_API_KEY_MAPPING = "appmetrica_app_api_key_mapping"
CONFIG_KEY_APPMETRICA_PROFILE_ID_APPS = "appmetrica_profile_id_apps"

CONFIG_KEY_APPSFLYER_APP_MAPPING = "appsflyer_app_id_mapping"
CONFIG_KEY_APPSFLYER_ID_MAPPING = "appsflyer_id_mapping"
CONFIG_KEY_APPSFLYER_DEV_KEY_MAPPING = "appsflyer_dev_key_mapping"


mappings = {
    "appsflyer_app_id_mapping": CONFIG_KEY_APPSFLYER_APP_MAPPING,
    "appsflyer_id_mapping": CONFIG_KEY_APPSFLYER_ID_MAPPING,
    "appsflyer_dev_key_mapping": CONFIG_KEY_APPSFLYER_DEV_KEY_MAPPING,

    "appmetrica_app_mapping": CONFIG_KEY_APPMETRICA_APP_MAPPING,
    "appmetrica_app_api_key_mapping" : CONFIG_KEY_APPMETRICA_APP_API_KEY_MAPPING,
    "appmetrica_profile_id_apps": CONFIG_KEY_APPMETRICA_PROFILE_ID_APPS,

    "app_s2s_keys_mapping": CONFIG_KEY_S2S_KEYS_MAPPING,

    "app_mapping": CONFIG_KEY_APP_MAPPING,
    "no_android_id_list": CONFIG_KEY_NO_ANDROID_ID,
    "ios_apps": CONFIG_KEY_IOS_APPS,
    "unique_loan_id_list": CONFIG_KEY_UNIQUE_LOAN,
    "allowed_sources_list": CONFIG_KEY_ALLOWED_SOURCES,
}


default_values = {
    "appsflyer_app_id_mapping": '{}',
    "appsflyer_id_mapping": '{}',
    "appsflyer_dev_key_mapping": '{}',

    "appmetrica_app_mapping": '{}',
    "appmetrica_app_api_key_mapping" : '{}',
    "appmetrica_profile_id_apps": '[]',

    "app_s2s_keys_mapping": '{}',

    "app_mapping": '{}',
    "no_android_id_list": '[]',
    "ios_apps": '[]',
    "unique_loan_id_list": '[]',
    "allowed_sources_list": '[]',
}