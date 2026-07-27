import time
from iot.mqtt_client import mqtt_client
from iot.topics import SENSOR_TOPIC

def cb(*args, **kwargs):
    print("CALLBACK")
    print(args)
    print(kwargs)

mqtt_client.connect()
mqtt_client.subscribe(
    topic=SENSOR_TOPIC,
    callback=cb,
)

print("Subscribed...")

while True:
    time.sleep(1)