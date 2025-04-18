import paho.mqtt.client as mqtt
import cv2
import numpy as np
from models.blaze_face import setup_model, detect_face


BROKER = "localhost"
PORT = 1883
TOPIC = "camera/frame"

model, processor = setup_model()


def on_message(client, userdata, msg):
    img_bytes = msg.payload
    np_array = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is not None:
        image = detect_face(model, processor, image)
        cv2.imshow("Received image", image)
        cv2.waitKey(1)




client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_forever()