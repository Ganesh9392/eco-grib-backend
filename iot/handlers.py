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
    """
    Handles incoming MQTT sensor messages.
    Supports:
    - Single JSON object
    - List of JSON objects
    """

    try:
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")

        data = json.loads(payload)

        print("\n" + "=" * 70)
        print("MQTT SENSOR MESSAGE RECEIVED")
        print("=" * 70)
        print(f"Topic   : {topic}")
        print(f"Payload : {json.dumps(data, indent=4)}")
        print("=" * 70)

        # If a list of sensor readings is received
        if isinstance(data, list):

            print(f"\nReceived {len(data)} sensor readings.\n")

            success = 0

            for reading in data:
                try:
                    sensor = save_sensor_reading(reading)
                    success += 1
                    print(
                        f"Saved Device {reading['deviceId']} -> ID {sensor.id}"
                    )
                except Exception as e:
                    print(
                        f"Failed Device {reading.get('deviceId')} : {e}"
                    )

            print(f"\nSuccessfully saved {success}/{len(data)} readings.\n")

        else:
            sensor = save_sensor_reading(data)

            print("\nSensor reading saved successfully.")
            print(f"Database ID : {sensor.id}\n")

    except json.JSONDecodeError:
        print("\nInvalid JSON received.\n")

    except Exception as e:
        print(f"\nHandler Error: {e}\n")