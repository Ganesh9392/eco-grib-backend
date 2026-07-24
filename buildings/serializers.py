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

    # NEW
    ambientLux = serializers.FloatField(source="ambient_lux")
    recommendedBrightness = serializers.IntegerField(
        source="recommended_brightness"
    )

    class Meta:
        model = Fixture
        fields = [
            "id",
            "device_id",                 # NEW
            "name",
            "building",
            "buildingName",
            "roomName",

            "motion",                    # NEW
            "ambientLux",                # NEW

            "isOn",
            "brightness",
            "recommendedBrightness",     # NEW

            "powerW",
            "voltageV",
            "currentA",
            "operatingHours",

            "health",
            "firmware",
            "status",

            "last_seen",                 # NEW

            "updated_at",
        ]

        read_only_fields = [
            "updated_at",
            "last_seen",
        ]

class FixtureControlSerializer(serializers.Serializer):

    is_on = serializers.BooleanField(required=False)

    brightness = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=100
    )

    recommended_brightness = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=100
    )

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                "Provide at least one field."
            )
        return data