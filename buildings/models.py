from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Building(models.Model):
    """A physical building/site (matches the frontend's Building type)."""

    class Status(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    floors = models.PositiveIntegerField(default=0)
    rooms = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONLINE)
    occupancy_rate = models.FloatField(default=0)  # 0.0 - 1.0

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


class Fixture(models.Model):
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
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="fixtures")
    room_name = models.CharField(max_length=150, blank=True, help_text="Simple room/location label")

    is_on = models.BooleanField(default=False)
    brightness = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="0-100 %",
    )

    power_w = models.FloatField(default=0)
    voltage_v = models.FloatField(default=0)
    current_a = models.FloatField(default=0)
    operating_hours = models.PositiveIntegerField(default=0)

    health = models.CharField(max_length=10, choices=Health.choices, default=Health.HEALTHY)
    firmware = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONLINE)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.building.name})"
