import datetime
import requests
from Models.geolocation import Geolocation
from Models.weather import Weather, WeatherForecast, WeatherType, MinMaxTemperature, DayTemperature
from Services.geo_service import GeoService
from typing import List
from Errors.auth_error import AuthError

WEATHER_TYPE_MAPPING = {
    "Thunderstorm" : WeatherType.THUNDERTORM,
    "Drizzle" : WeatherType.DRIZZLE,
    "Rain" : WeatherType.RAIN,
    "Snow" : WeatherType.SNOW,
    "Atmosphere" : WeatherType.ATMOSPHERE,
    "Clear" : WeatherType.CLEAR,
    "Clouds" : WeatherType.CLOUDS
}

class WeatherService:
    def __init__(self, api_key : str, geo_service : GeoService):
        self._api_key = api_key
        self._geo_service = geo_service


    def get_weather(self, city: str) -> Weather:
        location = self._geo_service.get_location(city)
        now, city = self._get_now(location)
        week, today = self._get_week_and_today(location)
        return Weather(now, today, week, city)


    def check_auth(self):
        self._get_now(Geolocation(0, 0, ""))


    def _get_now(self, location: Geolocation) -> (WeatherForecast, str):
        request = "https://api.openweathermap.org/data/2.5/weather?"\
                  f"lat={location.latitude}&" \
                  f"lon={location.longitude}&" \
                  f"units=metric&" \
                  f"lang=ru&" \
                  f"appid={self._api_key}"
        response = requests.get(request)
        data = response.json()
        self._check_data(data)
        weather = WeatherForecast(WEATHER_TYPE_MAPPING[data["weather"][0]["main"]],
                               data["main"]["temp"], datetime.datetime.now())
        return weather, data["name"]


    def _get_week_and_today(self, location: Geolocation) -> (List[WeatherForecast], DayTemperature):
        request = "https://api.openweathermap.org/data/2.5/onecall?" \
                  f"lat={location.latitude}&" \
                  f"lon={location.longitude}&" \
                  f"units=metric&" \
                  f"exclude=current,minutely,hourly,alerts&" \
                  f"appid={self._api_key}"
        response = requests.get(request)
        data = response.json()
        self._check_data(data)
        daily_data = data["daily"]

        today_data = daily_data[0]
        today_weather = DayTemperature(today_data["temp"]["morn"], today_data["temp"]["day"],
                                       today_data["temp"]["eve"], today_data["temp"]["night"])

        week_weather = []
        for day_data in daily_data:
            temperature = MinMaxTemperature(day_data["temp"]["min"], day_data["temp"]["max"])
            dt = day_data["dt"]
            weather_type = WEATHER_TYPE_MAPPING[day_data["weather"][0]["main"]]
            week_weather.append(WeatherForecast(weather_type,
                                                temperature,
                                                datetime.datetime.fromtimestamp(dt)))
        week_weather.pop(0) # remove weather for today from week weather

        return week_weather, today_weather


    def _check_data(self, data : dict):
        if "message" in data and "Invalid API key" in data["message"]:
            raise AuthError("OpenWeather")
