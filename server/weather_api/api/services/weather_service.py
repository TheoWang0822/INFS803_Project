from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
import requests

tf = TimezoneFinder()

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast/daily"
APP_ID = "188bc3753f510dd080520f8c14fd07d7"


def get_timezone(lat, lon):
    tz_str = tf.timezone_at(lat=lat, lng=lon)
    if not tz_str:
        raise Exception("Unable to determine timezone from coordinates.")
    return ZoneInfo(tz_str)


def get_weather_by_city_id(city_id):
    try:
        response = requests.get(API_BASE_URL, params={
            "id": city_id,
            "APPID": APP_ID,
            "units": "metric"
        }, timeout=5)
        response.raise_for_status()
        data = response.json()

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        local_tz = get_timezone(lat, lon)

        return {
            "id": data.get("id"),
            "cityname": data.get("name"),
            "temp": str(int(data["main"]["temp"])),
            "temp_min": str(int(data["main"]["temp_min"])),
            "temp_max": str(int(data["main"]["temp_max"])),
            "sun_raise": datetime.fromtimestamp(data["sys"]["sunrise"], tz=ZoneInfo("UTC")).astimezone(local_tz).strftime("%H:%M"), #get right timezone based on lat and lon
            "sun_set": datetime.fromtimestamp(data["sys"]["sunset"], tz=ZoneInfo("UTC")).astimezone(local_tz).strftime("%H:%M"), #get right timezone based on lat and lon
            "pressure": str(int(data["main"]["pressure"])),
            "humidy": str(int(data["main"]["humidity"])),
            "feels_like": str(int(data["main"]["feels_like"])),
            "detail_desc": data["weather"][0]["description"],
            "simp_desc": data["weather"][0]["main"]
        }
    except Exception as e:
        raise Exception(str(e))


def get_forecast_by_city_id(city_id):
    try:
        response = requests.get(FORECAST_API_URL, params={
            "id": city_id,
            "APPID": APP_ID,
            "units": "metric",
            "cnt": 7
        }, timeout=5)
        response.raise_for_status()
        data = response.json()

        lat = data["city"]["coord"]["lat"]
        lon = data["city"]["coord"]["lon"]
        local_tz = get_timezone(lat, lon)

        forecast_list = []
        for day in data.get("list", []):
            forecast_list.append({
                "date": datetime.fromtimestamp(day["dt"], tz=ZoneInfo("UTC")).astimezone(local_tz).strftime("%Y-%m-%d"), #get right timezone based on lat and lon
                "temp": str(int(day["temp"]["day"])),
                "temp_min": str(int(day["temp"]["min"])),
                "temp_max": str(int(day["temp"]["max"])),
                "simp_desc": day["weather"][0]["main"]
            })

        return forecast_list
    except Exception as e:
        raise Exception(str(e))
