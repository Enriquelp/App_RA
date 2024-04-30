import cv2
import socket
import pickle
import signal
import sys
import numpy as np
import threading

# Variables de red
ip = "127.0.0.1"
port_ArUco_Tracker = 6668
port_Filter_selector = 6669

# Variables Globales
LastCorners = ()
LastFrame = []
Continue = True

# Metodo para controlar la salida del script por ctrl+c
def handle_sigint(signal, frame):
    global Continue
    Continue = False
    print("Abortando ejecucion del microservicio.")
    sys.exit(0)  # Salir del script con código de salida 0

# Procesa el video y los datos del ArUco para mostrar la imagen superpuesta al ArUco
def process_video():
    global Continue
    if len(LastFrame) != 0 and LastCorners != (): # Si se detecta un codigo ArUco y hay video...
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

            #Mostramos el frame con la imagen sustituyendo al ArUco
            cv2.imshow("Visualizer", copy)
    else: # Si no hay videoo no se destecta codigo ArUco, se muestra una imagen que indica que no hay señal
        noImage = cv2.imread("Visualizer/media/NoSignal.webp")
        cv2.imshow("Visualizer", noImage)

    # Si se presiona q en la ventana, cerramos la ventana
    if cv2.waitKey(5) & 0xFF == ord('q'):
        # Cerramos la ventana
        Continue = False
        cv2.destroyAllWindows()

# Metodo que recibe los datos del ArUco
def receiveCorners():

    # Definimos la variable global para que le hilo pueda modificarla
    global LastCorners

    # Creamos el socket para recibir las coordenadas del ArUco Tracker
    s_ArUco_Tracker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_ArUco_Tracker.bind((ip, port_ArUco_Tracker))

    while Continue:
        try:
            # Ponemos un temporizador de 0.1 segundos
            s_ArUco_Tracker.settimeout(0.1)

            # Recibimos los datos del codigo ArUco
            msg_corners = s_ArUco_Tracker.recvfrom(1000000)
            clientip = msg_corners[1][0]
            data_corners_as_bytes = msg_corners[0]
            corners = pickle.loads(data_corners_as_bytes)
            LastCorners = corners
            
        except socket.timeout: # Si termina el temporizador sin recibir datos...
            print("Timeout: No se recibieron coordenadas dentro del tiempo especificado.") 
            LastCorners = ()
        except Exception as e:
            print("Error al recibir el video:", e)

# Metodo que recibe el stream de video
def receiveVideo():

    # Definimos la variable global para que le hilo pueda modificarla
    global LastFrame

     # Creamos el socket para recibir el video del Filter Selector
    s_Filter_selector = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_Filter_selector.bind((ip, port_Filter_selector))

    while Continue:
        try: 
            # Ponemos un temporizador de 0.1 segundos
            s_Filter_selector.settimeout(0.1)

            # Recibimos el stream de video
            msg_video = s_Filter_selector.recvfrom(1000000)
            clientip = msg_video[1][0]
            data_video_as_bytes = msg_video[0]

            # Convertir los datos del video recibidos a un frame de OpenCVS
            data_video = pickle.loads(data_video_as_bytes)
            frame = cv2.imdecode(data_video, cv2.IMREAD_COLOR)
            LastFrame = frame
        except socket.timeout: # Si termina el temporizador sin recibir datos...
            print("Timeout: No se recibió stream de video dentro del tiempo especificado.") 
            LastFrame = []
        except Exception as e:
            print("Error al recibir el video:", e)

# Metodo que inicia la ejecucion del microservicio
def start_service(): 

    # Creamos los hilos que se encargan de recibir los datos
    threadReceiveCorners = threading.Thread(target=receiveCorners)
    threadReceiveVideo = threading.Thread(target=receiveVideo)

    # Iniciamos la ejecucion de los hilos
    threadReceiveCorners.start()
    threadReceiveVideo.start()

    while Continue: 
        process_video()

    #Paramos la ejecucion del microservicio   
    cv2.destroyAllWindows()
    threadReceiveCorners.join()
    threadReceiveVideo.join()


signal.signal(signal.SIGINT, handle_sigint)
start_service()


