from django.urls import path
from api.views import StatusView, search_city_by_name

urlpatterns = [
    path('getStatus/', StatusView.as_view(), name='get-status'),
    path('SearchCityByName/', search_city_by_name, name='search-city-by-name'),
]