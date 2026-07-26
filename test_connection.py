from awsiot import mqtt_connection_builder

ENDPOINT = "a36l1k3v5e2fzy-ats.iot.eu-north-1.amazonaws.com"

connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath="certificates/ecogrid-main-controller.cert.pem",
    pri_key_filepath="certificates/ecogrid-main-controller.private.key",
    ca_filepath="certificates/AmazonRootCA1.pem",
    client_id="test-client",
    clean_session=True,
    keep_alive_secs=30,
)

print("Connecting...")

try:
    connection.connect().result()
    print("SUCCESS! Connected to AWS IoT.")

    connection.disconnect().result()
    print("Disconnected.")

except Exception as e:
    print("\nFAILED\n")
    print(type(e))
    print(e)