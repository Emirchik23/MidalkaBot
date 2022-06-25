from typing import NamedTuple

Geolocation = NamedTuple("Geolocation", [
    ("latitude", float),
    ("longitude", float),
    ("adress", str)
])
