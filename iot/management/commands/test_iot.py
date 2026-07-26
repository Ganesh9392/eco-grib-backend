from django.core.management.base import BaseCommand
from django.conf import settings
from awsiot import mqtt_connection_builder


class Command(BaseCommand):
    help = "Test AWS IoT connection"

    def handle(self, *args, **options):
        print("Starting AWS IoT test...")

        connection = mqtt_connection_builder.mtls_from_path(
            endpoint=settings.AWS_IOT_ENDPOINT,
            cert_filepath=str(settings.AWS_IOT_CERTIFICATE),
            pri_key_filepath=str(settings.AWS_IOT_PRIVATE_KEY),
            ca_filepath=str(settings.AWS_IOT_ROOT_CA),
            client_id="django-test-client",
            clean_session=True,
            keep_alive_secs=30,
        )

        try:
            print("Connecting...")
            connection.connect().result()
            print("✅ Connected successfully!")

            connection.disconnect().result()
            print("✅ Disconnected successfully!")

        except Exception as e:
            print("❌ Connection failed:")
            print(type(e))
            print(e)