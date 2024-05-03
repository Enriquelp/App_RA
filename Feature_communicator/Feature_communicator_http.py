import cv2
import requests
import numpy as np
import os
from flask import Flask, request

app = Flask(__name__)

own_port = os.environ.get("own_port", "5001")
ArUco_Tracker_ip = os.environ.get("ArUco_Tracker_ip", "127.0.0.1")
ArUco_Tracker_port = os.environ.get("ArUco_Tracker_port", "5002")
urlArUcoTracker = f'http://{ArUco_Tracker_ip}:{ArUco_Tracker_port}/ArucoTracker'

# Metodo para enviar el stream de video al ArUco_Tracker
def send_frame(gray_frame):
        
    # Codifica el frame en formato jpg y lo llamamos buffer
    success, buffer = cv2.imencode(".jpg", gray_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

    # Se envia el frame codificado al ArUco Tracker
    response = requests.post(urlArUcoTracker, data=buffer.tobytes(), headers={'Content-Type': 'image/jpeg'})

@app.route('/FeatureCommunicator', methods=['POST'])
def process_video():
    # Recibimos el stream de video
    data_video = request.data
    nparr = np.frombuffer(data_video, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Transformar el video a blanco y negro
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Enviamos el frame al ArUco_Tracler
    send_frame(gray_frame)

    return "OK", 200

if __name__ == '__main__':
    app.run(port=own_port)