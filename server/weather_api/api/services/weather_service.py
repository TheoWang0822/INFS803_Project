from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
import requests
from django.utils import timezone
from api.models import CityWeatherCurrent, CityWeatherForecast, CityList  

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
        one_hour_ago = timezone.now() - timedelta(hours=1)

        cached = CityWeatherCurrent.objects.filter(
            city_id=city_id,
            created_at__gte=one_hour_ago
        ).order_by('-created_at').first()

        if cached:
            local_tz = get_timezone(cached.lat, cached.lon)
            city = CityList.objects.get(id=city_id)
            return {
                "id": int(city_id),
                "cityname": city.cityname,
                "temp": str(int(cached.temp)),
                "temp_min": str(int(cached.temp_min)),
                "temp_max": str(int(cached.temp_max)),
                "sun_raise": cached.sunrise.astimezone(local_tz).strftime("%H:%M"),
                "sun_set": cached.sunset.astimezone(local_tz).strftime("%H:%M"),
                "pressure": str(cached.pressure),
                "humidy": str(cached.humidity),
                "feels_like": str(int(cached.temp_feels)),
                "detail_desc": cached.detail_desc,
                "simp_desc": cached.simple_desc
            }

        # Fetch from external API
        response = requests.get(API_BASE_URL, params={
            "id": city_id,
            "APPID": APP_ID,
            "units": "metric"
        }, timeout=5)
        print(response.url)
        response.raise_for_status()
        data = response.json()

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        local_tz = get_timezone(lat, lon)

        sunrise_utc = datetime.fromtimestamp(data["sys"]["sunrise"], tz=ZoneInfo("UTC"))
        sunset_utc = datetime.fromtimestamp(data["sys"]["sunset"], tz=ZoneInfo("UTC"))
        weather_date = timezone.now().date()

        CityWeatherCurrent.objects.create(
            city_id=city_id,
            data_dt=weather_date,
            temp=data["main"]["temp"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            sunrise=sunrise_utc,
            sunset=sunset_utc,
            pressure=data["main"]["pressure"],
            humidity=data["main"]["humidity"],
            temp_feels=data["main"]["feels_like"],
            detail_desc=data["weather"][0]["description"],
            simple_desc=data["weather"][0]["main"],
            lat=lat,
            lon=lon
        )

        return {
            "id": data.get("id"),
            "cityname": data.get("name"),
            "temp": str(int(data["main"]["temp"])),
            "temp_min": str(int(data["main"]["temp_min"])),
            "temp_max": str(int(data["main"]["temp_max"])),
            "sun_raise": sunrise_utc.astimezone(local_tz).strftime("%H:%M"),
            "sun_set": sunset_utc.astimezone(local_tz).strftime("%H:%M"),
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
        one_hour_ago = timezone.now() - timedelta(hours=1)

        cached = CityWeatherForecast.objects.filter(
            city_id=city_id,
            created_at__gte=one_hour_ago
        ).order_by('data_dt')

        if cached.count() >= 7:
            forecast_list = []
            city = CityList.objects.get(id=city_id)
            if cached.exists():
                first = cached.first()
                local_tz = get_timezone(first.cityweatherforecast.lat, first.cityweatherforecast.lon) if hasattr(first, 'lat') else ZoneInfo('UTC')
            else:
                local_tz = ZoneInfo('UTC')

            for entry in cached[:7]:
                forecast_list.append({
                    "date": entry.data_dt.strftime("%Y-%m-%d"),
                    "temp": str(int(entry.temp)),
                    "temp_min": str(int(entry.temp_min)),
                    "temp_max": str(int(entry.temp_max)),
                    "simp_desc": entry.simple_desc
                })
            return forecast_list

        # Fetch from external API
        response = requests.get(FORECAST_API_URL, params={
            "id": city_id,
            "APPID": APP_ID,
            "units": "metric",
            "cnt": 7
        }, timeout=5)
        print(response.url)
        response.raise_for_status()
        data = response.json()

        lat = data["city"]["coord"]["lat"]
        lon = data["city"]["coord"]["lon"]
        local_tz = get_timezone(lat, lon)

        forecast_list = []
        for day in data.get("list", []):
            date_obj = datetime.fromtimestamp(day["dt"], tz=ZoneInfo("UTC")).date()
            CityWeatherForecast.objects.create(
                city_id=city_id,
                data_dt=date_obj,
                temp=day["temp"]["day"],
                temp_min=day["temp"]["min"],
                temp_max=day["temp"]["max"],
                simple_desc=day["weather"][0]["main"]
            )
            forecast_list.append({
                "date": date_obj.strftime("%Y-%m-%d"),
                "temp": str(int(day["temp"]["day"])),
                "temp_min": str(int(day["temp"]["min"])),
                "temp_max": str(int(day["temp"]["max"])),
                "simp_desc": day["weather"][0]["main"]
            })

        return forecast_list

    except Exception as e:
        raise Exception(str(e))
