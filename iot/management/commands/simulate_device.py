from django.core.management.base import BaseCommand
from iot.device_simulator import main


class Command(BaseCommand):

    help = "Simulate ESP32"

    def handle(self, *args, **kwargs):
        main()