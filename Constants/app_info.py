import os.path
import appdirs

AUTHOR = "EmirhanMamedov"
NAME = "TelegramWeatherBot"

CONFIGS_DIR = appdirs.user_config_dir(NAME, AUTHOR)
AUTH_DATA_PATH = os.path.join(CONFIGS_DIR, "auth_data.json")