import cv2
import socket
import pickle
import signal
import sys
import numpy as np

ip = "127.0.0.1"
port = 6664

Visualizer_ip = "127.0.0.1"
Visualizer_port = 6669

# Metodo para controlar la salida del script por ctrl+c
def handle_sigint(signal, frame):
    print("Abortando ejecucion del microservicio.")
    sys.exit(0)  # Salir del script con código de salida 0

# Metodo para enviar el stream de video al ArUco_Tracker
def send_frame(frame, s_Visualizer):
    # Codifica el frame en formato jpg y lo llamamos buffer
    success, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    
    # Transforma a bytes el buffer
    frame_as_bytes = pickle.dumps(buffer)

    # Se envia el frame codificado al Visualizer
    try:
        s_Visualizer.sendto((frame_as_bytes), (Visualizer_ip, Visualizer_port))
    except Exception as e:
        print("Error al enviar el frame al ArUco_Tracker:", e)

def process_video(s_Video_Capturer, s_Visualizer):
    while True:
        try:
            # Configurar un timeout de 0.1 segundos
            s_Video_Capturer.settimeout(0.1)

            # Recibimos el stream de video
            x = s_Video_Capturer.recvfrom(1000000)
            clientip = x [1][0]
            data = x[0]

            # Convertir los datos recibidos a un frame de OpenCVS
            data = pickle.loads(data)
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

            # filtro de Blur
            frame = cv2.blur(frame, ksize=(50, 50))

            # Muestra la imagen con el filtro
            cv2.imshow("FilterSelector", frame)

            # Enviamos el frame al ArUco_Tracler
            send_frame(frame, s_Visualizer)

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
    # Establecemos la conexion socket UDP para el Visualizer
    s_Visualizer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.AF_INET -> Usamos IPv4, socket.SOCK_DGRAM -> usamos el protocolo UDP
    s_Visualizer.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000) # socket.SO_SNDBUF, 1000000 -> establece el tamaño de buffer de envio a 1MB
        # Creamos el socket para recibir el video del Video Capturer
    s_Video_Capturer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.AF_INET -> Usamos IPv4, socket.SOCK_DGRAM -> usamos el protocolo UDP
    s_Video_Capturer.bind((ip, port))
    
    while True:
        print("Esperando recepcion de video...")
        process_video(s_Video_Capturer, s_Visualizer)

signal.signal(signal.SIGINT, handle_sigint)
start_service()
