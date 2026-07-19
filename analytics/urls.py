from django.urls import path

from . import views

urlpatterns = [
    path("analytics/summary/", views.summary, name="analytics-summary"),
    path("analytics/energy/", views.energy_trend, name="analytics-energy"),
    path("analytics/by-building/", views.by_building, name="analytics-by-building"),
]
