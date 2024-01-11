import random
import time
from paho.mqtt import client as mqtt_client
import mysql.connector


broker = 'broker.emqx.io'
port = 1883
#topic = "python/mqtt"
topic = "varshaa/mqtt"
topic_publish = "varshaa_sub/mqtt"

# Database Configuration
db_host = 'localhost'
db_user = 'root'
db_password = 'Varshaa@114'
db_name = 'varshaadb'
table_name = 'mqtt_messages'


# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'

# Connect to the MySQL database
db_connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
cursor = db_connection.cursor()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("SUBSCRIBER-3 Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    my_list = [msg.payload.decode()]  # Assuming msg.payload is a bytes object
    print(f"Received `{my_list}` from topic `{msg.topic}`")
    store_message(my_list)
    publish()

def store_message(message):
        # Create a table (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mqtt_messages (
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                message VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    insert_query = f"INSERT INTO {table_name} (message) VALUES (%s)"
    try:
        cursor.execute(insert_query, message)
        db_connection.commit()
        print(f"Stored message in the database: {message}")
    except Exception as e:
        print(f"Error storing message in the database: {e}")
        db_connection.rollback()


def publish():
    msg = f"ACK"
    result = client.publish(topic_publish, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_publish}`")
    else:
        print(f"Failed to send message to topic {topic_publish}")


def subscribe(client: mqtt_client):
    client.subscribe(topic)
    client.on_message = on_message


if __name__ == '__main__':
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()