from Models.weather import WeatherType, Weather, WeatherForecast, TemperatureInfo, MinMaxTemperature, DayTemperature

START = '''Привет. Я умею показывать погоду — /show <city>. 
Если у меня не получается найти ваш город, укажите место подробнее (например: Казахстан Астана)'''

NO_CITY = "Укажите город или адрес вот так: /show <city>"
WEATHER_FORMAT = "%type_emoji%%temperature%, %type%"
WEATHER = '''%city%. 
Сейчас %now%
%today%

Погода на следующие 7 дней:
%week%'''

DAY_TEMPERATURE = '''Утром: %morning% C°
Днём: %afternoon% C°
Вечером: %evening% C°
Ночью: %night% C°
'''

LOCATION_NOT_FOUND = "Я не нашёл такого места на карте"

SCHEDULE_ARGS = "Укажите город и время чтобы установить расписание. Вот так: /set_schedule <city> <time>"
SCHEDULE_ALREAY_SET = "Расписание уже установлено на %time% для %city%. Вы можете иметь только одно расписание. " \
                      "Вы можете отменить существующее расписание (/cancel_schedule), а затем установить новое"
SCHEDULE_SET = "Успешно! Теперь я буду присылать вам погоду каждый день в %time%"
SCHEDULE_CANCEL = "Расписание отменено"
NO_SCHEDULE = "Расписание не установлено"
SCHEDULE_CAPTION = "Погода по расписанию"

REQUEST_ERROR = "Что-то пошло не так. Я не могу ответить на этот запрос"

WEATHER_TYPE_CAPTIONS = {
    WeatherType.CLEAR : "Ясно",
    WeatherType.ATMOSPHERE : "",
    WeatherType.CLOUDS : "Облачно",
    WeatherType.SNOW : "Снег",
    WeatherType.RAIN : "Дождь",
    WeatherType.DRIZZLE : "Ливень",
    WeatherType.THUNDERTORM : "Гроза"
}

WEATHER_TYPE_EMOJIS = {
    WeatherType.CLEAR : "☀️",
    WeatherType.ATMOSPHERE : "",
    WeatherType.CLOUDS : "☁️",
    WeatherType.SNOW : "🌨",
    WeatherType.RAIN : "🌧",
    WeatherType.DRIZZLE : "☔️",
    WeatherType.THUNDERTORM : "⚡️"
}

BOT_AUTH_ERROR = '''Ошибка авторизации бота. Не удалась авторизация в %service%. Возможно указан неправильный ключ/токен API.
Изменить настройки можно в %config%'''

class Formatter:
    @staticmethod
    def weather(weather : Weather) -> str:
        message = WEATHER.replace("%city%", weather.adress)\
            .replace("%now%", Formatter.weather_format(weather.now))\
            .replace("%today%", Formatter._format_temperature(weather.today))
        week_message = ""
        for w in weather.week:
            date = w.datetime.strftime("%d.%m.%Y")
            week_message += f"{date}: {Formatter.weather_format(w)}\n"
        message = message.replace("%week%", week_message)
        return message

    @staticmethod
    def weather_format(weather : WeatherForecast) -> str:
        return WEATHER_FORMAT.replace("%type_emoji%", WEATHER_TYPE_EMOJIS[weather.type])\
            .replace("%temperature%", Formatter._format_temperature(weather.temperature))\
            .replace("%type%", WEATHER_TYPE_CAPTIONS[weather.type])


    @staticmethod
    def bot_auth_error(service_name : str, config_path : str):
        return BOT_AUTH_ERROR.replace("%service%", service_name)\
            .replace("%config%", config_path)


    @staticmethod
    def _format_temperature(temperature : TemperatureInfo):
        if type(temperature) == float:
            result = f"{'%.2f' % temperature} C°"
        elif type(temperature) == MinMaxTemperature:
            result = f"{temperature.max} C° / {'%.2f' % temperature.min} C°"
        elif type(temperature) == DayTemperature:
            result = DAY_TEMPERATURE.replace("%morning%", '%.2f' % temperature.morning)\
                .replace("%afternoon%", '%.2f' % temperature.afternoon)\
                .replace("%evening%", '%.2f' % temperature.evening)\
                .replace("%night%", '%.2f' % temperature.night)
        else:
            raise Exception("Invalid temperature info")
        return result
