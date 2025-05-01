import paho.mqtt.client as mqtt
import cv2

BROKER = "localhost"
PORT = 1883
TOPIC = "camera/frame"

client = mqtt.Client()
client.connect(BROKER, PORT)

cap = cv2.VideoCapture("http://192.168.0.166:8080/video")

tick = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Something went wrong")
        break

    tick += 1

    if tick % 2 == 0:
        _, buffer = cv2.imencode(".jpg", frame)
        img_bytes = buffer.tobytes()

        client.publish(TOPIC, img_bytes)
        print("Data published")

cap.release()
client.disconnect()