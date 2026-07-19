from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("buildings", views.BuildingViewSet, basename="building")
router.register("fixtures", views.FixtureViewSet, basename="fixture")

urlpatterns = router.urls
