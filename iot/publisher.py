from .mqtt_client import mqtt_client
from .topics import CONTROL_TOPIC
from .utils import dict_to_json


def publish_control(payload):
    mqtt_client.publish(
        topic=CONTROL_TOPIC,
        payload=dict_to_json(payload),
    )