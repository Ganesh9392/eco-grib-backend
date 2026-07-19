from rest_framework import serializers


class BrightnessPredictionSerializer(serializers.Serializer):

    BuildingID = serializers.IntegerField()

    BuildingName = serializers.CharField()

    Floor = serializers.IntegerField()

    RoomID = serializers.CharField()

    RoomType = serializers.CharField()

    FixtureType = serializers.CharField()

    Occupancy = serializers.IntegerField()

    OccupancyCount = serializers.IntegerField()

    AmbientLux = serializers.FloatField()

    Hour = serializers.IntegerField()

    DayOfWeek = serializers.CharField()

    Month = serializers.IntegerField()

    Season = serializers.CharField()

    Weather = serializers.CharField()

    CurrentBrightness = serializers.FloatField()

    PreviousBrightness = serializers.FloatField()

    Energy_kWh = serializers.FloatField()

    Voltage_V = serializers.FloatField()

    Current_A = serializers.FloatField()

    PowerFactor = serializers.FloatField()

    OperatingHours = serializers.IntegerField()

    FixtureWattage = serializers.FloatField()

    UserOverrideCount = serializers.IntegerField()