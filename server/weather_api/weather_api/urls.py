from django.urls import path
from api.views import StatusView

urlpatterns = [
    path('getStatus/', StatusView.as_view(), name='get-status'),
]