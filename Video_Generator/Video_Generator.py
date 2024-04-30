import cv2
import socket
import pickle
import signal
import sys
import time

# Video a enviar
video_path = 'Video_Generator/media/PruebaVideo.avi'

# IP y puerto al que mandar el stream de video
feature_communicator_ip = "127.0.0.1"
feature_communicator_port = 6666
Filter_Selector_ip = "127.0.0.1"
Filter_Selector_port = 6664

# Metodo para controlar la salida del script por ctrl+c
def handle_sigint(signal, frame):
    print("Abortando ejecucion del microservicio.")
    sys.exit(0)  # Salir del script con código de salida 0

def send_video():
    while cap.isOpened():

        # Capturar un frame de la cámara
        success, frame = cap.read()  

        # Verifica si se ha alcanzado el final del video
        if not success:
            print("Video finalizado.")
            break

        # Abre una ventana mostrando el frame capturado de la camara
        cv2.imshow("videoGen", frame)

        # Codifica el frame en formato jpg y lo llamamos buffer
        success, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        
        # Transforma a bytes el buffer
        frame_as_bytes = pickle.dumps(buffer)

        # Se envia el frame codificado al feature_communicator
        try:
            s_Feature_Communicator.sendto((frame_as_bytes), (feature_communicator_ip, feature_communicator_port))
            s_Filter_Selector.sendto((frame_as_bytes), (Filter_Selector_ip, Filter_Selector_port))
        except Exception as e:
            print("Error al enviar el frame al Feature Communicator:", e)
    
        # Si se presiona q en la ventana, salimos del bucle
        if cv2.waitKey(5) & 0xFF == ord('q'):
            print("Envio de video finalizado...") 
            break
    
    # Liberar la cámara y cerrar la ventana
    cv2.destroyAllWindows()
    cap.release()
    

signal.signal(signal.SIGINT, handle_sigint)
# Establecemos la conexion socket UDP con Feature Communicator y Filter Selector
s_Feature_Communicator = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.AF_INET -> Usamos IPv4, socket.SOCK_DGRAM -> usamos el protocolo UDP
s_Feature_Communicator.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000) # socket.SO_SNDBUF, 1000000 -> establece el tamaño de buffer de envio a 1MB
s_Filter_Selector = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.AF_INET -> Usamos IPv4, socket.SOCK_DGRAM -> usamos el protocolo UDP
s_Filter_Selector.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000) # socket.SO_SNDBUF, 1000000 -> establece el tamaño de buffer de envio a 1MB

while True:
    # Crea un objeto VideoCapture para leer el archivo de video
    cap = cv2.VideoCapture(video_path)
    print("Enviando video...")
    send_video()
    time.sleep(2)