from django.db import models

from buildings.models import Building


class EnergyRecord(models.Model):
    """
    One row = how much energy one building used on one day.
    This simple daily table is enough to power all the analytics charts
    (daily load, monthly trend, building comparison) by summing/grouping
    in the view instead of storing lots of pre-computed tables.
    """

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="energy_records")
    date = models.DateField()
    kwh_used = models.FloatField(default=0)
    kwh_saved = models.FloatField(default=0)
    co2_reduced_kg = models.FloatField(default=0)

    class Meta:
        ordering = ["date"]
        unique_together = ["building", "date"]

    def __str__(self):
        return f"{self.building.name} - {self.date}: {self.kwh_used} kWh"
