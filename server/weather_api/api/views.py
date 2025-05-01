from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from .models import CityList

class StatusView(APIView):
    renderer_classes = [JSONRenderer]  # 确保返回 JSON

    def get(self, request):
        current_time = datetime.now().isoformat()  # 获取当前时间（ISO 格式）
        return Response(
            {"current_time": current_time},
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
def search_city_by_name(request):
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
