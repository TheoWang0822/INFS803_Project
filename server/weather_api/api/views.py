from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from .models import CityList
from api.services.weather_service import get_weather_by_city_id, get_forecast_by_city_id


class StatusView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        current_time = datetime.now().isoformat()
        return Response(
            {"current_time": current_time},
            status=status.HTTP_200_OK
        )

class SearchCityByNameView(APIView):
    def get(self, request):
        try:
            cityname = request.query_params.get('cityname', '').strip()
            if not cityname:
                return Response({"cities": []}, status=status.HTTP_200_OK)

            city_queryset = CityList.objects.filter(cityname__icontains=cityname)
            cities = [
                {"id": city.id, "cityname": city.cityname, "country": city.country}
                for city in city_queryset
            ]
            return Response({"cities": cities}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

class GetCurrentWeatherByCityView(APIView):

    def get(self, request):
        city_id = request.query_params.get('id', None)
        if not city_id:
            return Response({"error": "Missing 'id' parameter"}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = get_weather_by_city_id(city_id)
            if result and result.get("cityname"):
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response({"cities": []}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

class GetForecastWeatherByCityView(APIView):
    def get(self, request):
        city_id = request.query_params.get('id', None)
        if not city_id:
            return Response({"error": "Missing 'id' parameter"}, status=status.HTTP_404_NOT_FOUND)

        try:
            basic_info = get_weather_by_city_id(city_id)
            forecast_info = get_forecast_by_city_id(city_id)

            if basic_info and basic_info.get("cityname"):
                return Response({
                    "basic": basic_info,
                    "forecast": forecast_info
                }, status=status.HTTP_200_OK)
            else:
                return Response({"cities": []}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)