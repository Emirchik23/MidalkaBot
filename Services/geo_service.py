import requests

from Models.geolocation import Geolocation
from Errors.auth_error import AuthError
from Errors.location_not_found import LocationNotFound


class GeoService:
    def __init__(self, api_key : str):
        self._api_key = api_key


    def check_auth(self):
        self.get_location("Moscow")


    def get_location(self, adress : str) -> Geolocation:
        adress = adress.replace("?", "").replace("&", "")
        request = f"https://api.geoapify.com/v1/geocode/search?" \
                  f"text={adress}&" \
                  f"format=json&" \
                  f"limit=1&" \
                  f"apiKey={self._api_key}"
        response = requests.get(request)
        if response.status_code != 200:
            data = response.json()
            if "message" in data and "Invalid apiKey" in data["message"]:
                raise AuthError("Geoapify")
            raise Exception(f"Request error occured due geolocation request: {response.status_code}")
        results : list = response.json()["results"]
        if len(results) == 0:
            raise LocationNotFound()
        result = results[0]
        adress = f"{result['country']}"
        if 'state' in result:
            adress += f", {result['state']}"
        if 'city' in result:
            adress += f", {result['city']}"
        return Geolocation(result["lat"], result["lon"], adress)

