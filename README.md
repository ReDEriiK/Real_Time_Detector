# Real Time Detector Using IP Webcam
 ![ChatGPT Image 2025  ápr  18  11_17_14](https://github.com/user-attachments/assets/4c60ca33-ab9c-4aa7-ba3e-b3063c43819c)
> Image made by ChatGPT
 ## **Description**

This project was developed for a university course with the goal of building a real-time object detection application. It uses a smartphone as an IP webcam, transmitting video frames via MQTT using the Eclipse Mosquitto broker. The system is containerized with Docker and provides a web interface built with Flask for visualizing detection results in real time.

The object detection model is modular and can be easily replaced or extended by adding a new class to the models directory.

## **To run the project**

- Run the IP webcamn as a server on you phone

- ```docker-compose build```
- ```docker-compose up```
- Open ```localhost:5000```

## **To stop the container**

- ```docker-compose down```
