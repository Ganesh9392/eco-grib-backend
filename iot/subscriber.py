"""
MQTT Subscriber
"""

import time

from awscrt import mqtt

from .handlers import handle_sensor_message
from .mqtt_client import mqtt_client
from .topics import SENSOR_TOPIC


def _sensor_callback(topic, payload, **kwargs):
    print("\n" + "=" * 60)
    print("MESSAGE RECEIVED")
    print("=" * 60)
    print("Topic:", topic)
    print("Payload:", payload.decode())
    print("=" * 60)

    handle_sensor_message(topic, payload)


def start_subscriber():
    mqtt_client.connect()

    mqtt_client.subscribe(
        topic=SENSOR_TOPIC,
        callback=_sensor_callback,
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )

    print(f"Subscribed to {SENSOR_TOPIC}")
    print("Waiting for messages...")

    while True:
        time.sleep(1)