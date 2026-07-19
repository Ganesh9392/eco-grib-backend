from django.contrib import admin

from .models import Building, Fixture


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "floors", "rooms", "status", "occupancy_rate"]
    list_filter = ["status", "city"]
    search_fields = ["name", "city"]


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ["name", "building", "room_name", "is_on", "brightness", "status", "health"]
    list_filter = ["building", "status", "health", "is_on"]
    search_fields = ["name", "room_name"]
