from django.contrib import admin

from .models import Building, Fixture, SensorReading


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

# @admin.register(SensorReading)
# class SensorReadingAdmin(admin.ModelAdmin):
#     list_display = ["fixture", "created_at", "motion",]
#     list_filter = ["fixture", "created_at"]
#     search_fields = ["fixture__name"]

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    # Columns displayed in the list page
    list_display = (
        "id",
        "fixture",
        "device_id",
        "motion",
        "ambient_lux",
        "current_brightness",
        "reading_time",
        "created_at",
    )

    # Filters on the right side
    list_filter = (
        "motion",
        "fixture",
        "reading_time",
        "created_at",
    )

    # Search box
    search_fields = (
        "fixture__name",
        "device_id",
    )

    # Default ordering
    ordering = ("-reading_time",)

    # Read-only fields
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # Pagination
    list_per_page = 25

    # Clickable columns
    list_display_links = (
        "id",
        "fixture",
    )

    # Date hierarchy navigation
    date_hierarchy = "reading_time"

    # Field organization in detail page
    fieldsets = (
        ("Fixture Information", {
            "fields": (
                "fixture",
                "device_id",
            )
        }),
        ("Sensor Data", {
            "fields": (
                "motion",
                "ambient_lux",
                "current_brightness",
            )
        }),
        ("Reading Details", {
            "fields": (
                "reading_time",
            )
        }),
        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )
