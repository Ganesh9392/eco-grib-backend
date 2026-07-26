from django.core.management.base import BaseCommand
from iot.mqtt_client import mqtt_client


class Command(BaseCommand):
    help = "Test MQTT Wrapper"

    def handle(self, *args, **kwargs):
        mqtt_client.connect()
        print("Wrapper connected successfully.")
        mqtt_client.disconnect()
        print("Wrapper disconnected.")