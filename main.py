import bot_auth
import Constants.messages as messages
import Constants.app_info as app_info
from Services.bot_service import *
from Services.weather_service import *
from Services.geo_service import GeoService


def main():
    auth_data = bot_auth.default_auth()
    if auth_data == bot_auth.default_auth_data:
        print(f"Ключи API не указаны. Откройте {app_info.AUTH_DATA_PATH} и укажите их")
        return
    try:
        geo_service = GeoService(auth_data["geoapify_api_key"])
        geo_service.check_auth()
        weather_service = WeatherService(auth_data["open_weather_api_key"], geo_service)
        weather_service.check_auth()
        bot_token = auth_data["bot_token"]
        bot = BotService(bot_token, weather_service)
        bot.loop.create_task(wait_for_stop(bot))
        bot.run()
    except AuthError as error:
        print(messages.Formatter.bot_auth_error(error.service_name, app_info.AUTH_DATA_PATH))
    except Exception as error:
        print(f"Ошибка: {error}")
        print(f"Путь к конфигурации: {app_info.AUTH_DATA_PATH}")
        print("Сбросить конфигурацию (Это нельзя отменить) Y/N")
        answer = input()
        if (answer == "Y"):
            bot_auth.regenerate_config()
            main()
        else:
            quit()


async def wait_for_stop(bot : BotService):
    print("Бот запущен. Для остановки нажмите Enter")
    await asyncio.get_event_loop().run_in_executor(None, input)
    bot.loop.stop()


if __name__ == '__main__':
    main()