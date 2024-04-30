import cv2
import cv2
import numpy as np

# Función para dibujar un cubo en el frame
def draw_cube(img, corners):
    # Definir las coordenadas de los vértices del cubo
    cube_points = np.array([[-0.5, -0.5, 0], [-0.5, 0.5, 0], [0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, -0.5, 1], [-0.5, 0.5, 1], [0.5, 0.5, 1], [0.5, -0.5, 1]])
    cube_points = cube_points.reshape(-1, 3)

    # Definir la matriz de proyección
    mtx, dist = np.eye(3, 3), np.zeros(5)
    proj_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])

    # Proyectar los vértices del cubo en la imagen
    corners = np.squeeze(corners)
    retval, rvec, tvec = cv2.solvePnP(cube_points, corners, mtx, dist)

    # Proyectar los puntos del cubo en el plano de la imagen
    cube_points_2d, _ = cv2.projectPoints(cube_points, rvec, tvec, mtx, dist)

    # Dibujar líneas entre los puntos proyectados para formar el cubo
    imgpts = np.int32(cube_points_2d).reshape(-1, 2)
    img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)

    for i, j in zip(range(4), range(4, 8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (0, 255, 0), 3)

    img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 255, 0), -3)

    return img

# Cargar el video
cap = cv2.VideoCapture('Tests/PruebaVideo.avi')

# Cargar el clasificador de códigos ArUco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # Convertir el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los marcadores ArUco
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

        # Dibujar los códigos ArUco detectados
        frame = cv2.aruco.drawDetectedMarkers(frame, corners)

        # Dibujar un cubo encima de cada marcador ArUco
        #frame = draw_cube(frame, corners)
        print(f'Corners: {corners}')

        # Mostrar el frame con los marcadores detectados y el cubo de realidad aumentada
        cv2.imshow('Frame', frame)

        # Presionar 'q' para salir
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    else:
        break

# Liberar los recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
