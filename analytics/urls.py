from django.urls import path

from . import views

urlpatterns = [
    path("analytics/summary/", views.summary, name="analytics-summary"),
    path("analytics/energy/", views.energy_trend, name="analytics-energy"),
    path("analytics/by-building/", views.by_building, name="analytics-by-building"),
    path("analytics/daily-energy/", views.DailyEnergyAPIView.as_view(), name="analytics-by-daily"),
    path("analytics/monthly-energy/", views.MonthlyEnergyAPIView.as_view(), name="monthly-energy-report"),
    path("analytics/building-comparison/", views.BuildingComparisonAPIView.as_view(), name="building-energy-report"),
]
