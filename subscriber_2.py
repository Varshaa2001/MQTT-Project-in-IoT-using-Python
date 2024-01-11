import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "varshaa/mqtt"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("SUBSCRIBER-2 Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from topic `{msg.topic}`")


def subscribe(client: mqtt_client):
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()