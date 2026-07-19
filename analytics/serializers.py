from rest_framework import serializers

from .models import EnergyRecord


class EnergyRecordSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source="building.name", read_only=True)

    class Meta:
        model = EnergyRecord
        fields = ["id", "building", "building_name", "date", "kwh_used", "kwh_saved", "co2_reduced_kg"]
