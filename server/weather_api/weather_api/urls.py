from django.urls import re_path
from api.views import StatusView, SearchCityByNameView, GetCurrentWeatherByCityView, GetForecastWeatherByCityView, RegisterView, LoginView, LogoutView, GetUserProfileView

urlpatterns = [
    re_path(r'^GetStatus/?$', StatusView.as_view(), name='get-status'),
    re_path(r'^SearchCityByName/?$', SearchCityByNameView.as_view(), name='search-city-by-name'),
    re_path(r'^GetCurrentWeatherByCity/?$', GetCurrentWeatherByCityView.as_view(), name='get-current-weather-by-city'),
    re_path(r'^GetForecastWeatherByCity/?$', GetForecastWeatherByCityView.as_view(), name='get-forecast-weather-by-city'),
    re_path(r'^Register/?$', RegisterView.as_view(), name='register'),
    re_path(r'^Login/?$', LoginView.as_view(), name='login'),
    re_path(r'^Logout/?$', LogoutView.as_view(), name='logout'),
    re_path(r'^GetUserProfile/?$', GetUserProfileView.as_view(), name='get-user-profile'),
]