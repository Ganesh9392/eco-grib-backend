from rest_framework import serializers

from .models import Building, Fixture


class BuildingSerializer(serializers.ModelSerializer):
    fixtures = serializers.IntegerField(source="fixtures_count", read_only=True)
    energyKwh = serializers.FloatField(source="energy_kwh", read_only=True)
    occupancyRate = serializers.FloatField(source="occupancy_rate")

    class Meta:
        model = Building
        fields = [
            "id",
            "name",
            "address",
            "city",
            "floors",
            "rooms",
            "fixtures",
            "energyKwh",
            "status",
            "occupancyRate",
        ]


class FixtureSerializer(serializers.ModelSerializer):
    buildingName = serializers.CharField(source="building.name", read_only=True)
    roomName = serializers.CharField(source="room_name")
    isOn = serializers.BooleanField(source="is_on")
    powerW = serializers.FloatField(source="power_w")
    voltageV = serializers.FloatField(source="voltage_v")
    currentA = serializers.FloatField(source="current_a")
    operatingHours = serializers.IntegerField(source="operating_hours")

    class Meta:
        model = Fixture
        fields = [
            "id",
            "name",
            "building",
            "buildingName",
            "roomName",
            "isOn",
            "brightness",
            "powerW",
            "voltageV",
            "currentA",
            "operatingHours",
            "health",
            "firmware",
            "status",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]


class FixtureControlSerializer(serializers.Serializer):
    """
    Small serializer just for the brightness-control endpoint.
    Only accepts the two fields you're actually allowed to change remotely.
    """

    is_on = serializers.BooleanField(required=False)
    brightness = serializers.IntegerField(required=False, min_value=0, max_value=100)

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Provide at least 'is_on' or 'brightness'.")
        return data
