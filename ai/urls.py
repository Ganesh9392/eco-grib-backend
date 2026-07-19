from django.urls import path

from .views import BrightnessPredictionAPIView

urlpatterns = [
    path(
        "predict-brightness/",
        BrightnessPredictionAPIView.as_view(),
        name="predict-brightness",
    ),
]