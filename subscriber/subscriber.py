import time
from flask import Flask, render_template, Response
import cv2
import numpy as np
import threading
import paho.mqtt.client as mqtt
from models.blaze_face import setup_model, detect_face
import os

# --- Configuration ---
BROKER = os.getenv('MQTT_BROKER_HOST', 'mosquitto')
PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
TOPIC = os.getenv('MQTT_TOPIC', 'camera/frame')
client_id = f'receiver-{os.getpid()}'

latest_frame = None

model, processor = setup_model()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    global latest_frame
    while True:
        if latest_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Successfully connected to MQTT Broker at {BROKER}")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global latest_frame
    print("Message received on topic:", msg.topic)

    np_array = np.frombuffer(msg.payload, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if image is not None:
        image = detect_face(model, processor, image)
        ret, jpeg = cv2.imencode('.jpg', image)
        if ret:
            latest_frame = jpeg.tobytes()
    else:
        print("No image received")

def start_mqtt():
    print("Starting MQTT...")
    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    max_retries = 5
    retries = 0
    connected = False
    while not connected and retries < max_retries:
        try:
            client.connect(BROKER, PORT, 60)
            connected = True
        except Exception as e:
            retries += 1
            print(f"Connection attempt  failed")
            time.sleep(2)

    if not connected:
        print("Could not connect to MQTT broker after several retries. Exiting.")
        exit(1)

    print("Starting MQTT network loop...")
    client.loop_forever()


# --- Main Entry ---
if __name__ == '__main__':
    threading.Thread(target=start_mqtt, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)