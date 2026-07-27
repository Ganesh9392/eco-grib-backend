"""
MQTT Subscriber
"""

import time

from awscrt import mqtt

from .handlers import handle_sensor_message
from .mqtt_client import mqtt_client
from .topics import SENSOR_TOPIC


# def _sensor_callback(topic, payload, dup, qos, retain, **kwargs):
#     print("\n" + "=" * 80)
#     print("MQTT CALLBACK TRIGGERED")
#     print("=" * 80)

#     print(f"Topic   : {topic}")
#     print(f"Dup     : {dup}")
#     print(f"QoS     : {qos}")
#     print(f"Retain  : {retain}")

#     try:
#         if isinstance(payload, bytes):
#             print("Payload :")
#             print(payload.decode("utf-8"))
#         else:
#             print("Payload :")
#             print(payload)

#     except Exception as e:
#         print(f"Payload decode error: {e}")

#     print("=" * 80)

#     try:
#         handle_sensor_message(topic, payload)
#     except Exception as e:
#         print(f"Handler Exception: {e}")

def _sensor_callback(*args, **kwargs):
    print("\n" + "=" * 80)
    print("MQTT CALLBACK TRIGGERED")
    print("=" * 80)

    print("ARGS:")
    print(args)

    print("KWARGS:")
    print(kwargs)

    topic = None
    payload = None

    if len(args) >= 2:
        topic = args[0]
        payload = args[1]
    else:
        topic = kwargs.get("topic")
        payload = kwargs.get("payload")

    print("Topic:", topic)

    if isinstance(payload, bytes):
        print(payload.decode())
    else:
        print(payload)

    handle_sensor_message(topic, payload)


def start_subscriber():
    print("\nStarting MQTT Subscriber...\n")

    mqtt_client.connect()

    mqtt_client.subscribe(
        topic=SENSOR_TOPIC,
        callback=_sensor_callback,
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )

    print("\n" + "=" * 80)
    print(f"Subscribed to : {SENSOR_TOPIC}")
    print("Waiting for MQTT messages...")
    print("=" * 80)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping MQTT Subscriber...")
        mqtt_client.disconnect()