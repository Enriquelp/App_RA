import cv2
import socket
import pickle
import signal
import sys

ip = "127.0.0.1"
port = 6666

ArUco_Tracker_ip = "127.0.0.1"
ArUco_Tracker_port = 6667


# Metodo para controlar la salida del script por ctrl+c
def handle_sigint(signal, frame):
    print("Abortando ejecucion del microservicio.")
    sys.exit(0)  # Salir del script con código de salida 0

# Metodo para enviar el stream de video al ArUco_Tracker
def send_frame(gray_frame, s_ArUco_Tracker):
    # Codifica el frame en formato jpg y lo llamamos buffer
    success, buffer = cv2.imencode(".jpg", gray_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    
    # Transforma a bytes el buffer
    gray_frame_as_bytes = pickle.dumps(buffer)

    # Se envia el frame codificado al feature_communicator
    try:
        s_ArUco_Tracker.sendto((gray_frame_as_bytes), (ArUco_Tracker_ip, ArUco_Tracker_port))
    except Exception as e:
        print("Error al enviar el frame al ArUco_Tracker:", e)

def process_video(s_Video_Capturer, s_ArUco_Tracker):
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

            # Transformar el video a blanco y negro
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Muestra la imagen en blanco y negro
            cv2.imshow("featureComm", gray_frame)

            # Enviamos el frame al ArUco_Tracler
            send_frame(gray_frame, s_ArUco_Tracker)

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
    while True:
        # Establecemos la conexion socket UDP para el ArUco_Tracker
        s_ArUco_Tracker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.AF_INET -> Usamos IPv4, socket.SOCK_DGRAM -> usamos el protocolo UDP
        s_ArUco_Tracker.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000) # socket.SO_SNDBUF, 1000000 -> establece el tamaño de buffer de envio a 1MB
        # Creamos el socket para recibir el video del Video Capturer
        s_Video_Capturer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.AF_INET -> Usamos IPv4, socket.SOCK_DGRAM -> usamos el protocolo UDP
        s_Video_Capturer.bind((ip, port))
        print("Esperando recepcion de video...")
        process_video(s_Video_Capturer, s_ArUco_Tracker)
        s_ArUco_Tracker.close()
        s_Video_Capturer.close()

signal.signal(signal.SIGINT, handle_sigint)
start_service()
