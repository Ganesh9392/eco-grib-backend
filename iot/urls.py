from django.urls import path

from .views import IoTHealthAPIView

urlpatterns = [
    path("iot_health/", IoTHealthAPIView.as_view()),
]