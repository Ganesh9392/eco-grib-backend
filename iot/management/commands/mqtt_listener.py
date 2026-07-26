import time

from django.core.management.base import BaseCommand

from iot.subscriber import start_subscriber
from iot.mqtt_client import mqtt_client


class Command(BaseCommand):
    help = "Starts the AWS IoT MQTT Listener"

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.SUCCESS("Starting MQTT Listener...")
        )

        try:
            # Connect and subscribe
            start_subscriber()

            self.stdout.write(
                self.style.SUCCESS(
                    "MQTT Listener is running. Waiting for sensor data..."
                )
            )

            while True:
                time.sleep(1)

        except KeyboardInterrupt:

            self.stdout.write(
                self.style.WARNING("\nStopping MQTT Listener...")
            )

            mqtt_client.disconnect()

            self.stdout.write(
                self.style.SUCCESS("MQTT Listener stopped.")
            )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(f"\nMQTT Error: {e}")
            )

            mqtt_client.disconnect()