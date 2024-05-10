# Aplicación RA

Se trata de una aplicación de realidad aumentada que captura imagen desde una cámara, y con un código ArUco se muestra una imagen superpuesta a este código.

Esta aplicación estará gestionada por unos microservicios que reparten las diferentes tareas necesarias para su ejecución. El objetivo es poder desplegarlas en contenedores Docker sobre un orquestador (principalmente Kubernetes) en uno o varios dispositivos.

Se han desarrollado dos versiones de la aplicación. La primera, mas simple y solo de uso local sin usar contenedores, usa sockets para la comunicación entre los servicios. La segunda, que usa protocolo HTTP para la comunicación. Esta segunda versión es la principal y la que si se ha preparado para ejecutarse en contenedores y poder desplegarse en Kubernetes, aunque también puede ejecutarse en la maquina de forma local.

### Índice de contenidos

![Untitled](Diagrama_microservicios.png)

---

# Descripción de los Microservicios

- **Video Capturer:** Este microservicio se encarga exclusivamente de la captura video (sin sonido) desde una cámara web y de su posterior envio a las siguientes dos tareas (Feature Communicator y Filter Selector). Hace uso de la libreria OpenCV orientada a la visión por computador.
    
    Se puede configurar la resolución del video y los fotogramas por segundo (FPS).
    
- **Video Generator:** Cumple la misma función que el Video Generator pero enviando un video pregrabado en bucle, facilitando la ejecución de la aplicación si no se dispone de webcam.

- **Feature Communicator:** Inicia la linea de detección de elementos (códigos ArUco). Recibe el video y lo transforma a blanco y negro para enviárselo a la tarea de detección de elementos.

- **ArUco Tracker:** Busca códigos ArUco en el video recibido por el Feature Communicator, obteniendo sus identificadores y coordenadas asociadas para enviarlas al servidor de visualización.

- **Filter Selector:** Inicia la linea de visualización, aplicando un filtro de desenfoque y , posteriormente, manda el video modificado al servidor de visualización.

- **Visualizer:** Recibe el video modificado (del Filter Selector) y el identificador con las coordenadas de ArUco (del ArUco Tracker) para realizar la representación de una imagen 2D en tiempo real. Si no recibe datos de los dos al mismo tiempo, muestra una imagen que indica que no hay señal.
    
    La versión de sockets muestra el video generado por cada servicio en una ventana creada por openCV, y la versión HTTP solo muestra el video final en el navegador, en la ruta por defecto, [http://localhost:5003/visualizer](http://localhost:5003/visualizer) 
    

---

# Comunicación entre microservicios

los microservicios de la primera versión se comunican usando sockets. la razón para no usar WebSocket es que no se quiere crear una conexión constante ni bidireccional entre cliente y servidor, sino que cada microservicio esté pendiente de recibir datos, procesarlos y mandarlos al siguiente microservicio.

De esta forma cada microservicio debe conocer su propia IP (y puerto) y la IP (y puerto) al que va a enviar los datos.

Las dos excepciones a este comportamiento son el Video Capturer y el Visualizer; el primero solo envía datos (no los recibe) mientras el proceso esté activo, y el segundo solo recibe datos para procesarlos y mostrarlos.

Si algún microservicio falla durante el proceso, todos los demás quedan pendientes de recibir los datos para seguir el flujo normal de ejecución.

Existe una segunda versión de cada microservicio que usa http para la comunicación. En este caso, cada microservicio solo necesita conocer la IP y puerto al que enviará los datos.

---

# Ejecución de forma local (sin Docker)

Primero hay que instalar los requisitos en el entorno virtual. Para ello, ejecutamos:

```bash
python -v venv env # Crea el entorno virtual
.\env\Scripts\activate # Activa el entorno virtual (en windows)
pip install -r requirements.txt # Instala todas las dependencias del proyecto
```

Para ejecutar todos los microservicios de forma rápida y automática, se puede hacer doble clic sobre los archivos start.bat (para la versión de sockets) y startHTTP.bat (para la versión de http).

De forma alternativa, se puede lanzar un solo proceso ejecutando en la ubicación del script en un terminal la siguiente sentencia:

```python
python nombre_del_script.py
```

---

# Ejecución en Docker

Para crear y lanzar los contenedores de cada microservicio, hay que tener instalado Docker [para Windows](https://docs.docker.com/desktop/install/windows-install/) o [para Linux](https://docs.docker.com/desktop/install/linux-install/).

Primero creamos una red para que los contenedores puedan comunicarse entre ellos de forma local. De esta forma, no es necesario especificar las IPs de cada servicio, pues se pueden comunicar usando sus nombres como si de su IP se tratase.

```docker
docker network create my-network
```

 Con los siguientes comandos se crean las imagenes y los contenedores de cada uno de los microservicios.

- Video Generator
    
    ```docker
    docker build -t video_generator_http -f Video_Generator\dockerfile_VideoGenerator_http .
    docker run --network my-network -e "Feature_Communicator_ip=FeatureCommunicator" -e "Filter_Selector_ip=FilterSelector" --name VideoGenerator video_generator_http
    ```
    
- Video Capturer
    
    ```yaml
    docker build -t video_capturer_http -f Video_Capturer\dockerfile_VideoCapturer_http .
    docker run -v /dev/video0:/dev/video0 --network my-network -e "Feature_Communicator_ip=FeatureCommunicator" -e "Filter_Selector_ip=FilterSelector" --name VideoCapturer video_capturer_http
    ```
    
- Filter Selector
    
    ```docker
    docker build -t filter_selector_http -f Filter_Selector\dockerfile_FilterSelector_http .
    docker run --name FilterSelector -e "Visualizer_ip=Visualizer" --network my-network -p 5000:5000 filter_selector_http
    ```
    
- Feature Communicator
    
    ```docker
    docker build -t feature_communicator_http -f Feature_Communicator\dockerfile_FeatureCommunicator_http .
    docker run --name FeatureCommunicator -e "ArUco_Tracker_ip=ArUcoTracker" --network my-network -p 5001:5001 feature_communicator_http
    ```
    
- ArUco Tracker
    
    ```docker
    docker build -t aruco_tracker_http -f ArUco_Tracker\dockerfile_ArUcoTracker_http .
    docker run --name ArUcoTracker -e "Visualizer_ip=Visualizer" --network my-network -p 5002:5002 aruco_tracker_http 
    
    ```
    
- Visualizer
    
    ```docker
    docker build -t visualizer_http -f Visualizer\dockerfile_Visualizer_http . 
    docker run --name Visualizer --network my-network -p 5003:5003 visualizer_http
    ```
    

Para mayor comodidad, las imágenes ya han sido creadas y subidas a Docker Hub. Puedes encontrarlas en [este enlace](https://hub.docker.com/search?q=enriquelpzenc). Si deseas ejecutarlas descargándolas desde el Docker Hub, los comandos serian:

```yaml
docker run --name VideoGenerator --network my-network -e "Feature_Communicator_ip=FeatureCommunicator" -e "Filter_Selector_ip=FilterSelector" enriquelpzenc/video_generator_http
docker run --name VideoCapturer -v /dev/video0:/dev/video0 --network my-network -e "Feature_Communicator_ip=FeatureCommunicator" -e "Filter_Selector_ip=FilterSelector" enriquelpzenc/video_capturer_http
docker run --name FilterSelector -e "Visualizer_ip=Visualizer" --network my-network -p 5000:5000 enriquelpzenc/filter_selector_http
docker run --name FeatureCommunicator -e "ArUco_Tracker_ip=ArUcoTracker" --network my-network -p 5001:5001 enriquelpzenc/feature_communicator_http
docker run --name ArUcoTracker -e "Visualizer_ip=Visualizer" --network my-network -p 5002:5002 enriquelpzenc/aruco_tracker_http
docker run --name Visualizer --network my-network -p 5003:5003 enriquelpzenc/visualizer_http
```

[Dockerfiles](Documentacion/Dockerfiles.md)

---

[Despliegue de la aplicación RA en Kubernetes](Documentacion/Despliegue_de_la_aplicación_en_Kubernetes.md.md)