import json
import os
import Constants.app_info as app_info

default_auth_data = {
    "bot_token" : "",
    "open_weather_api_key" : "",
    "geoapify_api_key" : ""
}


def default_auth() -> dict:
    if not os.path.exists(app_info.CONFIGS_DIR):
        os.makedirs(app_info.CONFIGS_DIR)
    if not os.path.exists(app_info.AUTH_DATA_PATH):
        config_file = open(app_info.AUTH_DATA_PATH, "w")
        json.dump(default_auth_data, config_file)
        config_file.close()
    config_file = open(app_info.AUTH_DATA_PATH, "r")
    config = json.load(config_file)
    config_file.close()
    return config


def regenerate_config():
    if not os.path.exists(app_info.CONFIGS_DIR):
        os.makedirs(app_info.CONFIGS_DIR)
    config_file = open(app_info.AUTH_DATA_PATH, "w")
    json.dump(default_auth_data, config_file)
    config_file.close()
