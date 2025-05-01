import requests

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
APP_ID = "188bc3753f510dd080520f8c14fd07d7"

def get_weather_by_city_id(city_id):
    try:
        response = requests.get(API_BASE_URL, params={
            "id": city_id,
            "APPID": APP_ID,
            "units": "metric"
        }, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "id": data.get("id"),
            "cityname": data.get("name"),
            "temp": str(int(data["main"]["temp"])),
            "temp_min": str(int(data["main"]["temp_min"])),
            "temp_max": str(int(data["main"]["temp_max"])),
            "simp_desc": data["weather"][0]["main"]
        }
    except Exception as e:
        raise Exception(str(e))
