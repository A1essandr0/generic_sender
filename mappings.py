from libs.config_store import ConfigStore
import libs.constants as constants

mappings_dict = {
    constants.CONFIG_KEY_APP_MAPPING: ConfigStore().get_app_mapping,
    constants.CONFIG_KEY_NO_ANDROID_ID: ConfigStore().get_no_android_id_list,
    constants.CONFIG_KEY_IOS_APPS: ConfigStore().get_ios_apps,
    constants.CONFIG_KEY_UNIQUE_LOAN: ConfigStore().get_unique_loan_id_list,
    constants.CONFIG_KEY_S2S_KEYS_MAPPING: ConfigStore().get_app_s2s_keys_mapping,

    constants.CONFIG_KEY_ALLOWED_SOURCES: ConfigStore().get_allowed_sources_list,

    constants.CONFIG_KEY_APPMETRICA_APP_MAPPING: ConfigStore().get_appmetrica_app_mapping,
    constants.CONFIG_KEY_APPMETRICA_APP_API_KEY_MAPPING: ConfigStore().get_appmetrica_app_api_key_mapping,
    constants.CONFIG_KEY_APPMETRICA_PROFILE_ID_APPS: ConfigStore().get_appmetrica_profile_id_apps,

    constants.CONFIG_KEY_APPSFLYER_APP_MAPPING: ConfigStore().get_appsflyer_app_id_mapping,
    constants.CONFIG_KEY_APPSFLYER_ID_MAPPING: ConfigStore().get_appsflyer_id_mapping,
    constants.CONFIG_KEY_APPSFLYER_DEV_KEY_MAPPING: ConfigStore().get_appsflyer_dev_key_mapping,
}