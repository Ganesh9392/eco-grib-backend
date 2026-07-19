from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view
from rest_framework.response import Response

from buildings.models import Building, Fixture

from .models import EnergyRecord
from .serializers import EnergyRecordSerializer


@api_view(["GET"])
def summary(request):
    """
    GET /api/analytics/summary/

    One combined snapshot for the dashboard/analytics header cards:
    totals across all buildings and fixtures, plus energy used/saved.
    """
    totals = EnergyRecord.objects.aggregate(
        total_used=Sum("kwh_used"),
        total_saved=Sum("kwh_saved"),
        total_co2=Sum("co2_reduced_kg"),
    )

    fixtures = Fixture.objects.all()

    data = {
        "totalBuildings": Building.objects.count(),
        "totalFixtures": fixtures.count(),
        "onlineFixtures": fixtures.filter(status=Fixture.Status.ONLINE).count(),
        "offlineFixtures": fixtures.filter(status=Fixture.Status.OFFLINE).count(),
        "energyKwh": round(totals["total_used"] or 0, 2),
        "energySavedKwh": round(totals["total_saved"] or 0, 2),
        "carbonReducedKg": round(totals["total_co2"] or 0, 2),
    }
    return Response(data)


@api_view(["GET"])
def energy_trend(request):
    """
    GET /api/analytics/energy/?building=<id>&group=day|month

    Returns a time series for the energy charts. Defaults to daily,
    grouped by day. Pass group=month to get a monthly trend instead
    (used by the "Monthly Trend" chart).
    """
    qs = EnergyRecord.objects.all()

    building_id = request.query_params.get("building")
    if building_id:
        qs = qs.filter(building_id=building_id)

    group = request.query_params.get("group", "day")

    if group == "month":
        qs = (
            qs.annotate(period=TruncMonth("date"))
            .values("period")
            .annotate(kwh_used=Sum("kwh_used"), kwh_saved=Sum("kwh_saved"))
            .order_by("period")
        )
        return Response(list(qs))

    # default: plain daily rows
    qs = qs.order_by("date")
    return Response(EnergyRecordSerializer(qs, many=True).data)


@api_view(["GET"])
def by_building(request):
    """
    GET /api/analytics/by-building/

    Total usage/saved per building — feeds the "Building Comparison" chart.
    """
    qs = (
        EnergyRecord.objects.values("building__id", "building__name")
        .annotate(kwh_used=Sum("kwh_used"), kwh_saved=Sum("kwh_saved"))
        .order_by("-kwh_used")
    )
    data = [
        {
            "building": row["building__id"],
            "name": row["building__name"],
            "usage": round(row["kwh_used"] or 0, 2),
            "saved": round(row["kwh_saved"] or 0, 2),
        }
        for row in qs
    ]
    return Response(data)
