import json
import time

from awscrt import mqtt
from awsiot import mqtt_connection_builder
from django.conf import settings

from .topics import SENSOR_TOPIC


def main():

    connection = mqtt_connection_builder.mtls_from_path(
        endpoint=settings.AWS_IOT_ENDPOINT,
        cert_filepath=str(settings.AWS_IOT_CERTIFICATE),
        pri_key_filepath=str(settings.AWS_IOT_PRIVATE_KEY),
        ca_filepath=str(settings.AWS_IOT_ROOT_CA),
        client_id="simulator-client",
        clean_session=True,
        keep_alive_secs=30,
    )

    print("Connecting simulator...")
    connection.connect().result()
    print("Simulator connected.")

    payload = {
        "deviceId": "ESP001",
        "buildingId": "BLD001",
        "roomId": "ROOM101",
        "motion": True,
        "ambientLux": 320,
        "currentBrightness": 65,
        "temperature": 28.5,
        "humidity": 58,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    print(json.dumps(payload, indent=4))

    connection.publish(
        topic=SENSOR_TOPIC,
        payload=json.dumps(payload),
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )

    print("Published.")

    connection.disconnect().result()