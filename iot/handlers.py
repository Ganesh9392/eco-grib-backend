# import json

# from .services import save_sensor_reading


# def handle_sensor_message(topic, payload):
#     """
#     Handles incoming MQTT sensor messages.
#     """

#     try:
#         # AWS SDK sends bytes
#         if isinstance(payload, bytes):
#             payload = payload.decode("utf-8")

#         data = json.loads(payload)

#         print("\n" + "=" * 70)
#         print("MQTT SENSOR MESSAGE RECEIVED")
#         print("=" * 70)
#         print(f"Topic   : {topic}")
#         print(f"Payload : {json.dumps(data, indent=4)}")
#         print("=" * 70)

#         # Save into database
#         sensor = save_sensor_reading(data)

#         print(f"\nSensor reading saved successfully.")
#         print(f"Database ID : {sensor.id}\n")

#     except json.JSONDecodeError:
#         print("\nInvalid JSON received.\n")

#     except Exception as e:
#         print(f"\nHandler Error: {e}\n")










import json

from .services import save_sensor_reading


def handle_sensor_message(topic, payload):
    try:
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")

        data = json.loads(payload)

        print("\n" + "=" * 70)
        print("MQTT SENSOR MESSAGE RECEIVED")
        print("=" * 70)

        # If payload is a list
        if isinstance(data, list):
            print(f"Received {len(data)} sensor readings")

            for reading in data:
                sensor = save_sensor_reading(reading)
                print(f"Saved: {sensor.id}")

        # If payload is a single object
        else:
            sensor = save_sensor_reading(data)
            print(f"Saved: {sensor.id}")

    except json.JSONDecodeError:
        print("Invalid JSON")

    except Exception as e:
        print(f"Handler Error: {e}")