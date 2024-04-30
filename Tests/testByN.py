# muestra la imagen de la camara web en blanco y negro al acceder a http://127.0.0.1:5000/video_feed


from flask import Flask, request, Response
import cv2
import numpy as np

app = Flask(__name__)

def video_stream():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convertir el fotograma a blanco y negro
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Codificar el fotograma como JPEG
        ret, jpeg = cv2.imencode('.jpg', frame_bw)
        # Convertir a bytes
        frame_bytes = jpeg.tobytes()
        # Enviar el fotograma como respuesta
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
