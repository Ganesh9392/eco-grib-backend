import json


def json_to_dict(payload):
    return json.loads(payload)


def dict_to_json(data):
    return json.dumps(data)