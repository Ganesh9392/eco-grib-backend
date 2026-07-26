"""
Business Logic Layer

Responsibilities:
- Save sensor readings
- Update fixture state
- Trigger AI prediction (later)
- Publish control commands (later)
- Update analytics (later)
"""

from datetime import datetime

from django.utils import timezone

from buildings.models import Fixture, SensorReading


def save_sensor_reading(data):
    """
    Save incoming sensor data from AWS IoT Core.
    """

    device_id = data.get("deviceId")

    if not device_id:
        raise Exception("deviceId not found in MQTT payload.")

    try:
        fixture = Fixture.objects.get(device_id=device_id)

    except Fixture.DoesNotExist:
        raise Exception(f"No Fixture found for deviceId '{device_id}'")

    timestamp = data.get("timestamp")

    if timestamp:
        try:
            timestamp = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except Exception:
            timestamp = timezone.now()
    else:
        timestamp = timezone.now()

    # Update latest fixture status
    fixture.motion = data.get("motion", False)
    fixture.ambient_lux = data.get("ambientLux", 0)
    fixture.brightness = data.get("currentBrightness", 0)
    fixture.save()

    # Store historical sensor reading
    sensor = SensorReading.objects.create(
        fixture=fixture,
        motion=data.get("motion", False),
        ambient_lux=data.get("ambientLux", 0),
        current_brightness=data.get("currentBrightness", 0),
        reading_time=timestamp,
    )

    return sensor