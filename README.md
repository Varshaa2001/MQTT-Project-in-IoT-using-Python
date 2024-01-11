# MQTT-Project-in-IoT-using-Python

MQTT messaging using IOT

The main publisher sent the message to the MQTT broker, from the MQTT broker the message should be received to subscribers. There will be a publisher from the subscriber side. That Publisher will again send the message to the MQTT broker, From the MQTT broker the message will be received by the main Publisher.
About MQTT:

MQTT – Message Queuing Telemetry Transport.

⦁	It is a machine-to-machine protocol, i.e., it provides communication between the devices.
⦁	It is designed as a simple and lightweight messaging protocol that uses a publish/subscribe system to exchange information between the client and the server.
⦁	It does not require that both the client and the server establish a connection at the same time.
⦁	It provides faster data transmission, like how WhatsApp/messenger provides a faster delivery. It's a real-time messaging protocol.
⦁	It allows the clients to subscribe to a narrow selection of topics so that they can receive the information they are looking for.

MQTT Architecture

⦁	Message
⦁	Client
⦁	Server or Broker
⦁	TOPIC

A scenario where messages are being published from one MQTT client (taken as main publisher) to an MQTT Broker. Subscribers are listening for these messages, and one of the subscribers acts as a secondary publisher, sending messages back to the broker, which are then received by the main publisher. This can be achieved with the MQTT protocol and the paho- mqtt Python library. (pip install paho-mqtt)

Main Publisher:

⦁	Publishes messages to a specific topic on the MQTT broker.
⦁	Listens for messages from the MQTT broker, including messages published by the secondary publisher.

MQTT Broker:

⦁	Receives messages from the main publisher and forwards them to subscribers.
⦁	Accepts messages from the secondary publisher and forwards them to the main publisher and other subscribers.

Subscribers:

⦁	Subscribe to the topic on the MQTT broker where the main publisher is publishing messages.
⦁	One subscriber acts as a secondary publisher, sending messages back to the MQTT broker.

In this task, I have done by using Python code and created a main publisher and 2 subscribers and 1 secondary publisher which is also a one of the subscriber. I have taken broker as Open Source Distributed MQTT Broker - EMQX

broker = ‘broker.emqx.io'	

Running Process:

Run the First Subscriber Script:

Save the second script (the first subscriber) into a file, for example, subscriber1.py, This script will connect to the broker, subscribe to the specified topic, and print messages received on that topic.
Subcriber-1 connected to the broker(publish topic) – broker is ready to receive the messages.
 

Run the Second Subscriber Script:

Save the third script (the second subscriber) into a file, for example, subscriber2.py, This script will connect to the broker, subscribe to the specified topic, and print messages received on that topic.
Subcriber-2 connected to the broker (publish topic) – broker is ready to receive the messages.

 
Run the Secondary Publisher Script:

Save the fourth script (the secondary publisher) into a file, for example, subscriber 3.py, This script will connect to the broker, subscribe to the specified topic, and print messages received on that topic. And sends the topic to main publisher.
Subcriber-3 connected to the broker (publish topic) – broker is ready to receive the messages.
 

After running the main publisher (topic publishes to brokers) and broker will send to subscribers, in this case subscriber 3 is one of the secondary publisher it will receives the topic and stored in the database and sends topic to main publisher with Ack. The topic will received.

Relational Database (MySql) will shows table view that the received data with timestamp, I’ll take data as real-time process which is laptop’s microphone noise level.
 

Run the Main Publisher Script:

Save the first script (the main publisher) into a file, for example, main_publisher.py, This script will connect to the specified broker, publish messages to the specified topic, and exit after sending 10 messages.

 
