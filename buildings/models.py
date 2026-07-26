from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import TimeStampedModel, User


class Building(TimeStampedModel):
    """A physical building/site (matches the frontend's Building type)."""

    class Status(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="buildings")
    building_id = models.CharField(max_length=50, unique=True, help_text="Unique ID for this building/site")
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    floors = models.PositiveIntegerField(default=0, null=True, blank=True)
    rooms = models.PositiveIntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONLINE, null=True, blank=True)
    occupancy_rate = models.FloatField(default=0,null=True, blank=True)  # 0.0 - 1.0

    def __str__(self):
        return self.name

    @property
    def fixtures_count(self):
        return self.fixtures.count()

    @property
    def energy_kwh(self):
        """Total energy this building's fixtures are currently drawing (kW * hours not tracked here,
        this is just live power usage in kWh-equivalent for the dashboard cards)."""
        total_w = sum(f.power_w for f in self.fixtures.filter(is_on=True))
        return round(total_w / 1000, 2)

    def save(self, *args, **kwargs):
        if self.building_id is None or self.building_id == "":
            # Auto-generate a building_id if not provided
            last_building = Building.objects.order_by("-id").first()
            if last_building:
                last_id_num = int(last_building.building_id.replace("BLD", ""))
                self.building_id = f"BLD{last_id_num + 1:03d}"
            else:
                self.building_id = "BLD001"
        super().save(*args, **kwargs)             


class Fixture(TimeStampedModel):
    """
    A single light fixture that can be turned on/off and dimmed.
    This is the model behind the "Brightness Control" / Lighting page.
    """

    class Health(models.TextChoices):
        HEALTHY = "healthy", "Healthy"
        WARNING = "warning", "Warning"
        CRITICAL = "critical", "Critical"

    class Status(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"

    name = models.CharField(max_length=150)
    device_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique ESP32 / Controller ID",
        null=True,
        blank=True
    )
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="fixtures")
    room_name = models.CharField(max_length=150, blank=True, null=True, help_text="Simple room/location label")
    room_id = models.CharField(max_length=50, null=True, blank=True, help_text="Optional room/location ID for grouping fixtures")
    motion = models.BooleanField(null=True, blank=True, default=False, help_text="Whether motion is currently detected in this fixture's room")
    ambient_lux = models.FloatField(null=True, blank=True, default=0, help_text="Current ambient light level in lux")

    is_on = models.BooleanField(default=False)
    brightness = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="0-100 %",
        null=True,
        blank=True
    )

    power_w = models.FloatField(default=0, null=True, blank=True)
    voltage_v = models.FloatField(default=0, null=True, blank=True)
    current_a = models.FloatField(default=0, null=True, blank=True)
    operating_hours = models.PositiveIntegerField(default=0, null=True, blank=True)

    health = models.CharField(max_length=10, choices=Health.choices, default=Health.HEALTHY, null=True, blank=True)
    firmware = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONLINE, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.building.name})"


class SensorReading(TimeStampedModel):
    """
    Stores every sensor message received from AWS IoT Core.

    One MQTT message = One SensorReading record.
    This table is used for:
    - AI model training
    - Historical analytics
    - Energy reports
    - Occupancy analysis
    """

    fixture = models.ForeignKey(
        Fixture,
        on_delete=models.CASCADE,
        related_name="sensor_readings"
    )

    device_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique ESP32 / Controller ID",
        null=True,
        blank=True
    )

    motion = models.BooleanField(default=False)

    ambient_lux = models.FloatField(
        help_text="Ambient light level in Lux"
    )

    current_brightness = models.PositiveIntegerField(
        help_text="Current LED brightness (0-100%)"
    )

    reading_time = models.DateTimeField(
        help_text="Timestamp sent by the ESP32"
    )

    class Meta:
        ordering = ["-reading_time"]
        indexes = [
            models.Index(fields=["reading_time"]),
            models.Index(fields=["fixture"]),
        ]

    def __str__(self):
        return (
            f"{self.fixture.name} | "
            f"{self.current_brightness}% | "
            f"{self.reading_time}"
        )
