from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from .models import CityList, User
from api.services.weather_service import get_weather_by_city_id, get_forecast_by_city_id
from django.contrib.auth.hashers import make_password, check_password


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
                filtered_result = {
                    "id": result.get("id"),
                    "cityname": result.get("cityname"),
                    "temp": result.get("temp"),
                    "temp_min": result.get("temp_min"),
                    "temp_max": result.get("temp_max"),
                    "simp_desc": result.get("simp_desc")
                }
                return Response(filtered_result, status=status.HTTP_200_OK)
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
        
class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            username = data.get("username")
            password = data.get("password")
            avatar_id = data.get("avatar_id")
            email = data.get("email")

            if not all([username, password, email]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_404_NOT_FOUND)

            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already taken"}, status=status.HTTP_404_NOT_FOUND)

            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already in use"}, status=status.HTTP_404_NOT_FOUND)

            pwd_hash = make_password(password)

            User.objects.create(
                username=username,
                pwd_hash=pwd_hash,
                avatar_id=avatar_id,
                email=email
            )

            return Response({"success": True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response({"error": "Username and password are required"}, status=status.HTTP_404_NOT_FOUND)

            user = User.objects.filter(username=username).first()
            if user and check_password(password, user.pwd_hash):
                return Response({"success": True}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)