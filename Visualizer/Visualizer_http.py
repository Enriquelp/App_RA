import cv2
import pickle
import numpy as np
from flask import Flask, render_template, Response, request
import random
import os


app = Flask(__name__)

own_port = os.environ.get("own_port", "5003")

# Variables Globales
LastCorners = ()
Corners_random = 0 # Se usa para asignar un numero aleatorio cada vez que llegan nuevas esquinas
LastFrame = []
Frame_random = 0 # Se usa para asignar un numero aleatorio cada vez que llegan un nuevo frame

# Endpoint para mostrar el index.html
@app.route('/visualizer')
def index():
    return render_template('index.html')

# Endpoint encargado de servir el stream de video
@app.route('/video')
def video():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

def same_frame(auxFrames, auxCorners):

    if auxFrames != Frame_random and auxCorners != Corners_random:
        same = False
    else:
        same = True
    return same

# Procesa el video y los datos del ArUco para superponer la imagen al ArUco
def process_video():
    auxFrames = 0
    auxCorners = 0
    cont = 0
    same = False
    while True:

        # Controlamos cada cierto tiempo que hayan llegado nuevos frames
        if cont == 20:
            same = same_frame(auxFrames, auxCorners)
            auxFrames = Frame_random
            auxCorners = Corners_random
            cont = 0
        cont += 1

        if len(LastFrame) != 0 and LastCorners != () and not same: # Si se detecta un codigo ArUco y hay video, pero no son los de la anterior iteracion (han llegado nuevos)...

                # Extraemos las coordenadas de las esquinas
                c1 = (LastCorners[0][0][0][0], LastCorners[0][0][0][1])
                c2 = (LastCorners[0][0][1][0], LastCorners[0][0][1][1])
                c3 = (LastCorners[0][0][2][0], LastCorners[0][0][2][1])
                c4 = (LastCorners[0][0][3][0], LastCorners[0][0][3][1])

                # Hacemos una copia del frame
                copy = LastFrame

                # Cargamos la imagen a sobreponer en el codigo ArUco
                image = cv2.imread("Visualizer/media/dice_d20.png")

                # Extraemos el tamaño de la imagen
                image_size = image.shape

                # Ordenamos las esquinas del ArUco en una matriz
                aruco_corners = np.array([c1, c2, c3, c4])

                # Ordenamos las esquinas ded la imagen en otra matriz
                image_corners = np.array([
                    [0,0],
                    [image_size[1]-1, 0],
                    [image_size[1]-1, image_size[0]-1],
                    [0, image_size[0]-1]
                ], dtype = float)

                # Ponemos la imagen encima del codigo ArUco (Homografia)
                h, state = cv2.findHomography(image_corners, aruco_corners)

                # Controlamos la pespectiva (al inclinar el codigo ArUco)
                pespective = cv2.warpPerspective(image, h, (copy.shape[1], copy.shape[0]))
                cv2.fillConvexPoly(copy, aruco_corners.astype(int), 0, 16)
                copy = copy + pespective

                # Codifica el frame en formato jpg y lo llamamos buffer
                success, buffer = cv2.imencode('.jpg', copy)

                # Codificamos en bytes la imagen y la enviamos para mostrar en la web
                frame_as_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_as_bytes + b'\r\n')

        else: # Si no hay videoo no se destecta codigo ArUco, se muestra una imagen que indica que no hay señal
            # Leemos la imagen de "no hay señal"
            noImage = cv2.imread("Visualizer/media/NoSignal.webp")
            # Codifica el frame en formato jpg y lo llamamos buffer
            success, buffer = cv2.imencode('.jpg', noImage)
            # Codificamos en bytes la imagen y la enviamos para mostrar en la web
            noImage_as_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + noImage_as_bytes + b'\r\n')       
        
# Metodo que recibe los datos del ArUco
@app.route('/visualizer/receiveCorners', methods=['POST'])
def receiveCorners():

    # Declaramos que el metodo pueda modificar la variable global
    global LastCorners, Corners_random
    
    # Recibimos las esquinas del aruco y las decodificamos
    corners_as_bytes = request.data
    corners = pickle.loads(corners_as_bytes)

    LastCorners = corners
    Corners_random = random.uniform(1,1000000)

    return "OK", 200
            
# Metodo que recibe el stream de video
@app.route('/visualizer/receiveVideo', methods=['POST'])
def receiveVideo():

    # Declaramos que el metodo pueda modificar la variable global
    global LastFrame, Frame_random

    # Recibimos el stream de video y los decodificamos
    data_video = request.data
    nparr = np.frombuffer(data_video, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    LastFrame = frame
    Frame_random = random.uniform(1,1000000)

    return "OK", 200

if __name__ == '__main__':
    app.run(port=own_port)
    
    