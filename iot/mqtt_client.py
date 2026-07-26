from awscrt import mqtt
from awsiot import mqtt_connection_builder
from django.conf import settings


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
        except Exception as e:
            print(e)

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
        print(f"Published. Packet ID: {packet_id}")

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

        print("Subscription result:", result)
        print("Packet:", packet_id)

mqtt_client = MQTTClient()