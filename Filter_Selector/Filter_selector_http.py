import cv2
import numpy as np
import requests
import os
from flask import Flask, request

app = Flask(__name__)

own_host = os.environ.get("own_host", "127.0.0.1")
own_port = os.environ.get("own_port", "5000")
Visualizer_ip = os.environ.get("Visualizer_ip", "127.0.0.1")
Visualizer_port = os.environ.get("Visualizer_port", "5003")
urlVisualizer = f'http://{Visualizer_ip}:{Visualizer_port}/visualizer/receiveVideo'

# Metodo para enviar el stream de video al ArUco_Tracker
def send_frame(frame):

    # Codifica el frame en formato jpg y lo llamamos buffer
    success, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

    # Se envia el frame codificado al Visualizer
    response = requests.post(urlVisualizer, data=buffer.tobytes(), headers={'Content-Type': 'image/jpeg'})
    
@app.route('/FilterSelector', methods=['POST'])
def process_video():

    # Recibimos el stream de video
    data_video = request.data
    nparr = np.frombuffer(data_video, np.uint8)
    gray_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Aplicamos el filtro de desenfoque (blur)
    frame_with_filter = cv2.blur(gray_frame, ksize=(50, 50))

    # Enviamos el frame al ArUco_Tracler
    send_frame(frame_with_filter)

    return "OK", 200

if __name__ == '__main__':
    app.run(host=own_host, port=own_port)
