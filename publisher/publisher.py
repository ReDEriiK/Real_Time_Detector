import paho.mqtt.client as mqtt
import cv2
import os
import time

BROKER = os.getenv('MQTT_BROKER_HOST', 'mosquitto')
PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
TOPIC = os.getenv('MQTT_TOPIC', 'camera/frame')
client_id = f'sender-{os.getpid()}'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Successfully connected to MQTT Broker at {BROKER}")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect

try:
    client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"Error connecting to MQTT Broker: {e}")
    exit(1)

client.loop_start()

time.sleep(2)

cap = cv2.VideoCapture("http://192.168.0.194:8080/video")
tick = 0
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Something went wrong")
            break

        tick += 1

        if tick % 2 == 0:
            _, buffer = cv2.imencode(".jpg", frame)
            img_bytes = buffer.tobytes()

            result = client.publish(TOPIC, img_bytes)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Data published to topic {TOPIC}")
            else:
                print(f"Failed to publish the data to topic {TOPIC}")
except KeyboardInterrupt:
    print("Publisher stopping...")
finally:
    client.loop_stop()
    client.disconnect()
    cap.release()
    print("Publisher disconnected")