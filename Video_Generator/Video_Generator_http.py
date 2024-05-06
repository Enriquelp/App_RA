import cv2
import requests
import time
import os

# Video a enviar
video_path = 'Video_Generator/media/PruebaVideo.avi'

# IPs y puertos a los que mandar el stream de video
Feature_Communicator_ip = os.environ.get("Feature_Communicator_ip", "127.0.0.1")
Feature_Communicator_port = os.environ.get("Feature_Communicator_port", "5001")
Filter_Selector_ip = os.environ.get("Filter_Selector_ip", "127.0.0.1")
Filter_Selector_port = os.environ.get("Filter_Selector_port", "5000")
urlFeatureCommunicator = f'http://{Feature_Communicator_ip}:{Feature_Communicator_port}/FeatureCommunicator'
urlFilterSelector = f'http://{Filter_Selector_ip}:{Filter_Selector_port}/FilterSelector'



def send_video():
    while cap.isOpened():

        # Capturar un frame de la cámara
        success, frame = cap.read()  

        # Verifica si se ha alcanzado el final del video
        if not success:
            print("Video finalizado.")
            break

        # Abre una ventana mostrando el frame capturado de la camara
        #cv2.imshow("videoGen", frame)

        # Codifica el frame en formato jpg y lo llamamos buffer
        success, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

        # Se envia el frame codificado al Feature Communicator y al Filter Selector
        try:
            responseFeatureCommunicator = requests.post(urlFeatureCommunicator, data=buffer.tobytes(), headers={'Content-Type': 'image/jpeg'})
            responseFilterSelector = requests.post(urlFilterSelector, data=buffer.tobytes(), headers={'Content-Type': 'image/jpeg'})
        except Exception as e:
            print("Error al enviar stream de video: ", e)
            break
    
        # Si se presiona q en la ventana, salimos del bucle
        if cv2.waitKey(5) & 0xFF == ord('q'):
            print("Envio de video finalizado...") 
            break
    
    # Liberar la cámara y cerrar la ventana
    cv2.destroyAllWindows()
    cap.release()   

while True:
    # Crea un objeto VideoCapture para leer el archivo de video
    cap = cv2.VideoCapture(video_path)
    print("Enviando video...")
    send_video()
    time.sleep(2)