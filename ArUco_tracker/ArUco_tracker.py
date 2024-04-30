import cv2
import socket
import pickle
import signal
import sys

ip = "127.0.0.1"
port = 6667

Visualizer_ip = "127.0.0.1"
Visualizer_port = 6668

# Metodo para controlar la salida del script por ctrl+c
def handle_sigint(signal, frame):
    print("Abortando ejecucion del microservicio.")
    sys.exit(0)  # Salir del script con código de salida 0

# Metodo para enviar los datos del ArUco al Visualizer
def send_corners(corners, ids, s_Visualizer):
    
    corners_as_bytes = pickle.dumps(corners)

    # Se envia el frame codificado al feature_communicator
    try:
        s_Visualizer.sendto((corners_as_bytes), (Visualizer_ip, Visualizer_port))
    except Exception as e:
        print("Error al enviar el frame al ArUco_Tracker:", e)

#Metodo para buscar codigos ArUco en el video
def search_ArUco(gray_frame):
    # Detectar los marcadores ArUco
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray_frame)

    # Dibujar los códigos ArUco detectados
    frame = cv2.aruco.drawDetectedMarkers(gray_frame, corners)
    return corners, ids, frame

# Metodo para buscar el codigo ArUco en el video
def process_video(s_feature_communicator, s_Visualizer):
    while True:
        try:
            # Configurar un timeout de 0.1 segundos
            s_feature_communicator.settimeout(0.1)

            # Recibimos el stream de video
            x = s_feature_communicator.recvfrom(1000000)
            clientip = x [1][0]
            data = x[0]

            # Convertir los datos recibidos a un frame de OpenCVS
            data = pickle.loads(data)
            gray_frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

            # detectamos el codigo ArUco en el video
            corners, ids ,arUco_frame = search_ArUco(gray_frame)

            # Muestra la imagen en blanco y negro
            cv2.imshow("ArUcoTracker", arUco_frame)

            # Enviamos los datos al Visualizer
            send_corners(corners, ids, s_Visualizer)

             # si se presiona q en la ventana, cerramos la ventana y salimos del bucle
            if cv2.waitKey(5) & 0xFF == ord('q'):
                # Cerramos la ventana
                cv2.destroyAllWindows()
                break
        except socket.timeout:
            print("Timeout: No se recibieron nuevos datos dentro del tiempo especificado.")
            break
        except Exception as e:
            print("Error al recibir el video:", e)
            break
    # Cerramos la ventana
    cv2.destroyAllWindows()



def start_service():
     # Establecemos la conexion socket UDP para el ArUco_Tracker
    s_Visualizer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.AF_INET -> Usamos IPv4, socket.SOCK_DGRAM -> usamos el protocolo UDP
    s_Visualizer.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000) # socket.SO_SNDBUF, 1000000 -> establece el tamaño de buffer de envio a 1MB
    # Creamos el socket para recibir el video del Feature Communicator
    s_feature_communicator = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_feature_communicator.bind((ip, port))

    while True:
        print("Esperando recepcion de video...")
        process_video(s_feature_communicator, s_Visualizer)

signal.signal(signal.SIGINT, handle_sigint)

# Cargar el clasificador de códigos ArUco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
start_service()

