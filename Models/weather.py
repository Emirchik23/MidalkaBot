import datetime
from enum import Enum
from typing import NamedTuple
from typing import Dict
from typing import List
from typing import Union


class WeatherType(Enum):
    CLEAR = 0
    CLOUDS = 1
    RAIN = 2
    THUNDERTORM = 3
    DRIZZLE = 4
    ATMOSPHERE = 5
    SNOW = 6


MinMaxTemperature = NamedTuple("MinMaxTemperature", [
    ("min", float),
    ("max", float),
])


DayTemperature = NamedTuple("DayTemperature", [
    ("morning", float),
    ("afternoon", float),
    ("evening", float),
    ("night", float),
])


TemperatureInfo = Union[float, MinMaxTemperature, DayTemperature]


WeatherForecast = NamedTuple("WeatherForecast", [
    ("type", WeatherType),
    ("temperature", TemperatureInfo),
    ("datetime", datetime.datetime)
])


Weather = NamedTuple("Weather", [
    ("now", WeatherForecast),
    ("today", DayTemperature),
    ("week", List[WeatherForecast]),
    ("adress", str)
])

