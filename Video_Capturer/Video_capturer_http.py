import cv2
import requests
import os

# IPs y puertos a los que mandar el stream de video
Feature_Communicator_ip = os.environ.get("Feature_Communicator_ip", "127.0.0.1")
Feature_Communicator_port = os.environ.get("Feature_Communicator_port", "5001")
Filter_Selector_ip = os.environ.get("Filter_Selector_ip", "127.0.0.1")
Filter_Selector_port = os.environ.get("Filter_Selector_port", "5000")
urlFeatureCommunicator = f'http://{Feature_Communicator_ip}:{Feature_Communicator_port}/FeatureCommunicator'
urlFilterSelector = f'http://{Filter_Selector_ip}:{Filter_Selector_port}/FilterSelector'

# Parametros del video
image_width = os.environ.get("image_width", "640")
image_height = os.environ.get("image_height", "480")
image_FPS = os.environ.get("image_FPS", "30")

def send_video():
    while cap.isOpened():
        success, frame = cap.read()  # Capturar un frame de la cámara
        if not success:
            break

        # Abre una ventana mostrando el frame capturado de la camara
        cv2.imshow("videoCap", frame)

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
            print("Captura de video finalizada...")
            break

    # Liberar la cámara y cerrar la ventana
    cv2.destroyAllWindows()
    cap.release()


print("Capturando video...")
while True:
    # Configurar la captura de video desde la cámara web
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(image_width)) # Ancho del video
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(image_height)) # Alto del video
    cap.set(cv2.CAP_PROP_FPS, int(image_FPS)) # FPS del video
    send_video()