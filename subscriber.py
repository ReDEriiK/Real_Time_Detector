from flask import Flask, render_template, Response
import cv2
import numpy as np
import threading
import paho.mqtt.client as mqtt
from models.blaze_face import setup_model, detect_face

# --- Configuration ---
BROKER = "localhost"
PORT = 1883
TOPIC = "camera/frame"
latest_frame = None

# --- Model Setup ---
model, processor = setup_model()

# --- Flask App ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Frame Generator ---
def generate():
    global latest_frame
    while True:
        if latest_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code:", rc)
    client.subscribe(TOPIC)

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

def start_mqtt():
    print("Starting MQTT...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_forever()

# --- Main Entry ---
if __name__ == '__main__':
    threading.Thread(target=start_mqtt, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)