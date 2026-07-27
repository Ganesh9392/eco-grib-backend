from awscrt import mqtt
from awsiot import mqtt_connection_builder
from django.conf import settings


def on_connection_interrupted(connection, error, **kwargs):
    print("\n========== CONNECTION INTERRUPTED ==========")
    print(f"Error: {error}")
    print("============================================\n")


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("\n========== CONNECTION RESUMED ==========")
    print(f"Return Code    : {return_code}")
    print(f"Session Present: {session_present}")

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session lost. Re-subscribing...")

        connection.resubscribe_existing_topics().result()

        print("Re-subscribed successfully.")

    print("========================================\n")


class MQTTClient:
    def __init__(self):
        self.connection = None
        self.connected = False

    def connect(self):
        if self.connected and self.connection:
            return self.connection

        print("\n========== AWS IoT ==========")
        print(f"Endpoint : {settings.AWS_IOT_ENDPOINT}")
        print(f"Client ID: {settings.AWS_IOT_CLIENT_ID}")
        print("=============================\n")

        self.connection = mqtt_connection_builder.mtls_from_path(
            endpoint=settings.AWS_IOT_ENDPOINT,
            cert_filepath=str(settings.AWS_IOT_CERTIFICATE),
            pri_key_filepath=str(settings.AWS_IOT_PRIVATE_KEY),
            ca_filepath=str(settings.AWS_IOT_ROOT_CA),
            client_id=settings.AWS_IOT_CLIENT_ID,
            clean_session=True,
            keep_alive_secs=30,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
        )

        print("Connecting to AWS IoT Core...")
        self.connection.connect().result()

        self.connected = True

        print("Connected successfully.\n")

        return self.connection

    def disconnect(self):
        if not self.connection:
            return

        try:
            print("Disconnecting...")
            self.connection.disconnect().result()
            print("Disconnected.")
        except Exception as e:
            print(f"Disconnect Error: {e}")

        self.connection = None
        self.connected = False

    def publish(self, topic, payload):
        self.connect()

        future, packet_id = self.connection.publish(
            topic=topic,
            payload=payload,
            qos=mqtt.QoS.AT_LEAST_ONCE,
        )

        future.result()

        print(f"Published to '{topic}'")
        print(f"Packet ID: {packet_id}")

    def subscribe(
        self,
        topic,
        callback,
        qos=mqtt.QoS.AT_LEAST_ONCE,
    ):
        self.connect()

        future, packet_id = self.connection.subscribe(
            topic=topic,
            qos=qos,
            callback=callback,
        )

        result = future.result()

        print("\n========== SUBSCRIPTION ==========")
        print(f"Topic     : {topic}")
        print(f"Packet ID : {packet_id}")
        print(f"Result    : {result}")
        print("==================================\n")


mqtt_client = MQTTClient()