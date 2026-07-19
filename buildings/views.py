from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Building, Fixture
from .serializers import BuildingSerializer, FixtureControlSerializer, FixtureSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    """
    GET/POST   /api/buildings/
    GET/PATCH/DELETE /api/buildings/{id}/
    """

    queryset = Building.objects.all().order_by("name")
    serializer_class = BuildingSerializer


class FixtureViewSet(viewsets.ModelViewSet):
    """
    GET/POST   /api/fixtures/
    GET/PATCH/DELETE /api/fixtures/{id}/

    Optional filter: /api/fixtures/?building=<id>
    """

    queryset = Fixture.objects.all().order_by("name")
    serializer_class = FixtureSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        building_id = self.request.query_params.get("building")
        if building_id:
            qs = qs.filter(building_id=building_id)
        return qs

    @action(detail=True, methods=["patch"])
    def control(self, request, pk=None):
        """
        PATCH /api/fixtures/{id}/control/   { "is_on": true, "brightness": 70 }

        This is the endpoint the brightness slider / on-off switch on the
        Lighting page talks to.
        """
        fixture = self.get_object()
        serializer = FixtureControlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if "is_on" in serializer.validated_data:
            fixture.is_on = serializer.validated_data["is_on"]
            if not fixture.is_on:
                fixture.brightness = 0

        if "brightness" in serializer.validated_data:
            fixture.brightness = serializer.validated_data["brightness"]
            fixture.is_on = fixture.brightness > 0

        fixture.save()
        return Response(FixtureSerializer(fixture).data)

    @action(detail=False, methods=["post"])
    def bulk_control(self, request):
        """
        POST /api/fixtures/bulk_control/   { "is_on": true, "building": 1 }

        Turns every online fixture on/off at once (the "All ON" / "All OFF"
        buttons on the Lighting page). "building" is optional — omit it to
        control every building.
        """
        is_on = request.data.get("is_on")
        if is_on is None:
            return Response({"detail": "'is_on' is required."}, status=400)

        qs = Fixture.objects.filter(status=Fixture.Status.ONLINE)
        building_id = request.data.get("building")
        if building_id:
            qs = qs.filter(building_id=building_id)

        updated = qs.update(is_on=bool(is_on), brightness=60 if is_on else 0)
        return Response({"updated": updated})
