from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from datetime import datetime

class StatusView(APIView):
    renderer_classes = [JSONRenderer]  # 确保返回 JSON

    def get(self, request):
        current_time = datetime.now().isoformat()  # 获取当前时间（ISO 格式）
        return Response(
            {"current_time": current_time},
            status=status.HTTP_200_OK
        )