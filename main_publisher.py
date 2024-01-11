import random
import time
import pyaudio
import numpy as np

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "varshaa/mqtt"
topic_subscribe = "varshaa_sub/mqtt"
# Generate a Client ID with the publish prefix.
main_publisher_client_id = f'publish-{random.randint(0, 1000)}' # Publish data to all the 3 subscriberss

def record_audio(duration=5, channels=1, rate=44100):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=1024)

   # print("Recording...")

    frames = []

    for i in range(int(rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

   # print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.frombuffer(b''.join(frames), dtype=np.int16)

def calculate_noise_level(audio_signal):
    # Calculate the root mean square (RMS) of the audio signal
    rms = np.sqrt(np.mean(audio_signal.astype(np.int64) ** 2))
    return rms

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MAIN PUBLISHER connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from topic `{msg.topic}`")

def connect_mqtt():
    client = mqtt_client.Client(main_publisher_client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
        # Continuous monitoring
    try:
        while True:
            audio_signal = record_audio()
            noise_level = calculate_noise_level(audio_signal)
            msg = f"Noise level : {noise_level}"
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            time.sleep(1)  # You can adjust the sleep duration as needed

    except KeyboardInterrupt:
        print("Monitoring stopped.")

def subscribe(client: mqtt_client):
    client.subscribe(topic_subscribe)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    publish(client)
    time.sleep(30)
    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    run()