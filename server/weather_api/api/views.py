from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from .models import CityList, User, UserFavorite
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
            is_default = request.query_params.get('is_default', '').strip()
            cityname = request.query_params.get('cityname', '').strip()

            if is_default == '1':
                city_queryset = CityList.objects.filter(is_default=True)
            elif cityname:
                city_queryset = CityList.objects.filter(cityname__icontains=cityname)
            else:
                return Response({"cities": []}, status=status.HTTP_200_OK)

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
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.pwd_hash):

            request.session['user_id'] = user.id
            request.session.set_expiry(60 * 60 * 24 * 30) 
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)
        
class LogoutView(APIView):
    def post(self, request):
        try:
            request.session.flush()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
class GetUserProfileView(APIView):
    def get(self, request):
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return Response({}, status=status.HTTP_200_OK)

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({}, status=status.HTTP_200_OK)

            favorites = UserFavorite.objects.filter(user_id=user.id)
            city_ids = [fav.city_id for fav in favorites]
            cities = CityList.objects.filter(id__in=city_ids)

            city_data = [
                {"id": city.id, "cityname": city.cityname, "country": city.country}
                for city in cities
            ]

            return Response({
                "basic": {
                    "username": user.username,
                    "avatar_id": str(user.avatar_id) if user.avatar_id else "",
                    "email": user.email
                },
                "favorite_cities": city_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
class AddFavoriteCityView(APIView):
    def post(self, request):
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return Response({"error": "User not logged in"}, status=status.HTTP_404_NOT_FOUND)

            city_id = request.data.get("cityid")
            if not city_id:
                return Response({"error": "Missing 'cityid'"}, status=status.HTTP_404_NOT_FOUND)

            # Check if city exists
            city = CityList.objects.filter(id=city_id).first()
            if not city:
                return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

            # Prevent duplicates
            existing = UserFavorite.objects.filter(user_id=user_id, city_id=city_id).first()
            if not existing:
                UserFavorite.objects.create(user_id=user_id, city_id=city_id)

            return Response({
                "favorite_cities": _get_favorite_cities(user_id)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class DelFavoriteCityView(APIView):
    def delete(self, request):
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return Response({"error": "User not logged in"}, status=status.HTTP_404_NOT_FOUND)

            city_id = request.data.get("cityid")
            if not city_id:
                return Response({"error": "Missing 'cityid'"}, status=status.HTTP_404_NOT_FOUND)

            UserFavorite.objects.filter(user_id=user_id, city_id=city_id).delete()

            return Response({
                "favorite_cities": _get_favorite_cities(user_id)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


def _get_favorite_cities(user_id):
    favorites = UserFavorite.objects.filter(user_id=user_id)
    city_ids = [fav.city_id for fav in favorites]
    cities = CityList.objects.filter(id__in=city_ids)

    return [
        {"id": city.id, "cityname": city.cityname, "country": city.country}
        for city in cities
    ]
