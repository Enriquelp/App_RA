import cv2
import pickle
import numpy as np
import requests
from flask import Flask, request

app = Flask(__name__)

own_port = 5002

Visualizer_ip = "127.0.0.1"
Visualizer_port = 5003
urlVisualizer = f'http://{Visualizer_ip}:{Visualizer_port}/visualizer/receiveCorners'

# Cargar el clasificador de códigos ArUco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Metodo para enviar los datos del ArUco al Visualizer
def send_corners(corners, ids):

    corners_as_bytes = pickle.dumps(corners)
    # Se envia el frame codificado al feature_communicator
    response = requests.post(urlVisualizer, data=corners_as_bytes)


#Metodo para buscar codigos ArUco en el video
def search_ArUco(gray_frame):
    # Detectar los marcadores ArUco
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray_frame)

    # Dibujar los códigos ArUco detectados
    frame = cv2.aruco.drawDetectedMarkers(gray_frame, corners)
    return corners, ids, frame

# Metodo para buscar el codigo ArUco en el video
@app.route('/ArucoTracker', methods=['POST'])
def process_video():

    # Recibimos el stream de video
    data_video = request.data
    nparr = np.frombuffer(data_video, np.uint8)
    gray_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # detectamos el codigo ArUco en el video
    corners, ids, arUco_frame = search_ArUco(gray_frame)

    # Enviamos los datos de las esquinas al Visualizer
    send_corners(corners, ids)

    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True, port=own_port)