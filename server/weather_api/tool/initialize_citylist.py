import os
import sys
import django
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_api.settings")
django.setup()

from api.models import CityList
from django.utils import timezone

json_file_path = os.path.join(os.path.dirname(__file__), 'current.city.list.json')

def load_city_data():
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    current_time = timezone.now()

    inserted_count = 0
    skipped_count = 0

    for item in data:
        cityname = item.get('name')
        country = item.get('country')
        city_id = item.get('id')

        if CityList.objects.filter(cityname=cityname).exists():
            skipped_count += 1
            continue

        city = CityList(
            id=city_id,
            cityname=cityname,
            is_default=False,
            country=country,
            created_at=current_time
        )
        city.save()
        inserted_count += 1

    print(f"Inserted: New {inserted_count} items, skipped {skipped_count} existing records.")

if __name__ == "__main__":
    load_city_data()
