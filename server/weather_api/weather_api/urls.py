from django.urls import re_path
from api.views import StatusView, SearchCityByNameView, GetCurrentWeatherByCityView, GetForecastWeatherByCityView, RegisterView, LoginView

urlpatterns = [
    re_path(r'^getStatus/?$', StatusView.as_view(), name='get-status'),
    re_path(r'^SearchCityByName/?$', SearchCityByNameView.as_view(), name='search-city-by-name'),
    re_path(r'^GetCurrentWeatherByCity/?$', GetCurrentWeatherByCityView.as_view(), name='get-current-weather-by-city'),
    re_path(r'^GetForecastWeatherByCity/?$', GetForecastWeatherByCityView.as_view(), name='get-forecast-weather-by-city'),
    re_path(r'^register/?$', RegisterView.as_view(), name='register'),
    re_path(r'^login/?$', LoginView.as_view(), name='login'),
]