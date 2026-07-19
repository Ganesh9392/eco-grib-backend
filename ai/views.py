from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BrightnessPredictionAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        return Response(
            {
                "message": "AI model has not been trained yet."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )