import cv2
import mediapipe as mp

def setup_model():
    mp_face_detection = mp.solutions.face_detection
    model = mp_face_detection.FaceDetection(model_selection=0)
    processor = None
    return model, processor

def detect_face(model, processor, image):
    results = model.process(image)
    
    if results.detections is not None:
        for detection in results.detections:
            box = detection.location_data.relative_bounding_box
            print(box)
            h, w, c = image.shape
            x_min, y_min = box.xmin * w, box.ymin * h
            width_box, height_box = box.width * w, box.height * h
            print(type(image))
            print(x_min, y_min)
            print(x_min + width_box, y_min + height_box)
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_min + width_box), int(y_min + height_box)), (0, 255, 0), 2)

    return image


if __name__=="__main__":
    image = cv2.imread("D:\Real_Time_Face_Detector\pic_01.png")
    model, processor = setup_model()
    print(type(image))
    results = detect_face(model, processor, image)
    cv2.imshow("Received image", image)
    cv2.waitKey(0)