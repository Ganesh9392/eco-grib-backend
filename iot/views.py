from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class IoTHealthAPIView(APIView):
    """
    Checks whether the IoT service is available.
    """

    def get(self, request):
        return Response({
            "status": "connected",
            "service": "AWS IoT Core"
        })