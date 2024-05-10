# Dockerfiles

- dockerfile_VideoGenerator_http.yaml
    
    ```docker
    # Usa la imagen base de Python
    FROM python:latest
    
    # Copia el script al contenedor
    COPY Video_Generator/Video_generator_http.py /app/Video_Generator/Video_generator_http.py
    COPY Video_Generator/media /app/Video_Generator/media
    COPY ../requirements.txt /app/requirements.txt
    
    # Establece el directorio de trabajo
    WORKDIR /app
    
    # Instala las dependencias necesarias, como OpenCV
    RUN apt-get update
    RUN apt install -y libgl1-mesa-glx
    RUN pip install -r requirements.txt
    
    # Establece las variables de entorno
    ENV Feature_Communicator_ip="0.0.0.0" \
        Feature_Communicator_port="5001" \
        Filter_Selector_ip="0.0.0.0" \
        Filter_Selector_port="5000"
    
    # Comando para ejecutar el script
    CMD ["python", "Video_Generator/Video_generator_http.py"]
    
    ```
    
- dockerfile_VideoCapturer_http.yaml
    
    ```yaml
    # Usa la imagen base de Python
    FROM python:latest
    
    # Copia el script al contenedor
    COPY Video_Capturer/Video_capturer_http.py /app/Video_capturer_http.py
    COPY ../requirements.txt /app/requirements.txt
    
    # Establece el directorio de trabajo
    WORKDIR /app
    
    # Instala las dependencias necesarias, como OpenCV
    RUN apt-get update
    RUN apt install -y libgl1-mesa-glx
    RUN pip install -r requirements.txt
    
    # Establece las variables de entorno
    ENV Feature_Communicator_ip="0.0.0.0" \
        Feature_Communicator_port="5001" \
        Filter_Selector_ip="0.0.0.0" \
        Filter_Selector_port="5000"
    
    # Comando para ejecutar el script
    CMD ["python", "Video_capturer_http.py"]
    ```
    
- dockerfile_FilterSelector_http.yaml
    
    ```yaml
    # Usa la imagen base de Python
    FROM python:latest
    
    # Copia el script al contenedor
    COPY Filter_Selector/Filter_selector_http.py /app/Filter_Selector/Filter_selector_http.py
    COPY ../requirements.txt /app/requirements.txt
    
    # Establece el directorio de trabajo
    WORKDIR /app
    
    # Instala las dependencias necesarias, como OpenCV
    RUN apt-get update
    RUN apt install -y libgl1-mesa-glx
    RUN pip install -r requirements.txt
    
    # Establece las variables de entorno
    ENV own_host="0.0.0.0" \
        own_port="5000" \
        Visualizer_ip="0.0.0.0" \
        Visualizer_port="5003"
    
    # Abrimos el puerto 5000 del contenedor para permitir las comunicaciones
    EXPOSE 5000
    
    # Comando para ejecutar el script
    CMD ["python", "Filter_Selector/Filter_selector_http.py"]
    
    ```
    
- dockerfile_FeatureCommunicator_http.yaml
    
    ```yaml
    # Usa la imagen base de Python
    FROM python:latest
    
    # Copia el script al contenedor
    COPY Feature_Communicator/Feature_communicator_http.py /app/Feature_Communicator/Feature_communicator_http.py
    COPY ../requirements.txt /app/requirements.txt
    
    # Establece el directorio de trabajo
    WORKDIR /app
    
    # Instala las dependencias necesarias, como OpenCV
    RUN apt-get update
    RUN apt install -y libgl1-mesa-glx
    RUN pip install -r requirements.txt
    
    # Establece las variables de entorno
    ENV own_host="0.0.0.0" \
        own_port="5001" \
        ArUco_Tracker_ip="0.0.0.0" \
        ArUco_Tracker_port="5002"
    
    # Abrimos el puerto 5001 del contenedor para permitir las comunicaciones
    EXPOSE 5001
    
    # Comando para ejecutar el script
    CMD ["python", "Feature_Communicator/Feature_communicator_http.py"]
    ```
    
- dockerfile_ArUcoTracker_http.yaml
    
    ```yaml
    # Usa la imagen base de Python
    FROM python:latest
    
    # Copia el script al contenedor
    COPY ArUco_Tracker/ArUco_tracker_http.py /app/ArUco_Tracker/ArUco_tracker_http.py
    COPY ../requirements.txt /app/requirements.txt
    
    # Establece el directorio de trabajo
    WORKDIR /app
    
    # Instala las dependencias necesarias, como OpenCV
    RUN apt-get update
    RUN apt install -y libgl1-mesa-glx
    RUN pip install -r requirements.txt
    
    # Establece las variables de entorno
    ENV own_host="0.0.0.0" \
        own_port="5002" \
        Visualizer_ip="0.0.0.0" \
        Visualizer_port="5003"
    
    # Abrimos el puerto 5002 del contenedor para permitir las comunicaciones
    EXPOSE 5002 
    
    # Comando para ejecutar el script
    CMD ["python", "ArUco_Tracker/ArUco_tracker_http.py"]
    ```
    
- dockerfile_Visualizer_http.yaml
    
    ```yaml
    # Usa la imagen base de Python
    FROM python:latest
    
    # Copia el script al contenedor
    COPY Visualizer/Visualizer_http.py /app/Visualizer/Visualizer_http.py
    COPY Visualizer/media /app/Visualizer/media
    COPY Visualizer/templates /app/Visualizer/templates
    COPY ../requirements.txt /app/requirements.txt
    
    # Establece el directorio de trabajo
    WORKDIR /app
    
    # Instala las dependencias necesarias, como OpenCV
    RUN apt-get update
    RUN apt install -y libgl1-mesa-glx
    RUN pip install -r requirements.txt
    
    # Establece las variables de entorno
    ENV own_port="5003" \
        own_host="0.0.0.0"
    
    # Abrimos el puerto 5003 del contenedor para permitir las comunicaciones
    EXPOSE 5003
    
    # Comando para ejecutar el script
    CMD ["python", "Visualizer/Visualizer_http.py"]
    ```