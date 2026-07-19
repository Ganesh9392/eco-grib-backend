from django.contrib import admin

from .models import EnergyRecord


@admin.register(EnergyRecord)
class EnergyRecordAdmin(admin.ModelAdmin):
    list_display = ["building", "date", "kwh_used", "kwh_saved", "co2_reduced_kg"]
    list_filter = ["building"]
    date_hierarchy = "date"
