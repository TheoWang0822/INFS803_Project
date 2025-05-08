from django.urls import path
from api.views import StatusView, SearchCityByNameView, GetCurrentWeatherByCityView, GetForecastWeatherByCityView

urlpatterns = [
    path('getStatus/', StatusView.as_view(), name='get-status'),
    path('SearchCityByName/', SearchCityByNameView.as_view(), name='search-city-by-name'),
    path('GetCurrentWeatherByCity/', GetCurrentWeatherByCityView.as_view(), name='get-current-weather-by-city'),
    path('GetForecastWeatherByCity/', GetForecastWeatherByCityView.as_view(), name='get-forecast-weather-by-city'),
]