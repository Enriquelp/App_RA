# YAMLs Kubernetes

- VideoGenerator.yaml
    
    ```yaml
    # video-generator-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: video-generator
    spec: # Configuracion del deployment
      replicas: 1 # Indica el número deseado de réplicas del conjunto de pods que el Deployment debe mantener en funcionamiento en todo momento.
      selector: # Especifica cómo el Deployment encuentra qué pods administrar. 
        matchLabels: # Define las etiquetas que deben coincidir con las etiquetas de los pods para que sean seleccionados por este Deployment. 
          app: video-generator
      template: # Define la plantilla para crear nuevos pods administrados por el Deployment.
        metadata:
          labels: # Especifica las etiquetas que se asignarán a los pods creados por este Deployment.
            app: video-generator
        spec:
          containers:
          - name: video-generator # Nombre del contenedor
            image: enriquelpzenc/video_generator_http:latest # Imagen usada para el contenedor.
            env: # Variables del servicio.
              - name: Feature_Communicator_ip
                value: "192.168.49.2"
              - name: Feature_Communicator_port
                value: "30001"
              - name: Filter_Selector_ip
                value: "192.168.49.2" 
              - name: Filter_Selector_port
                value: "30000"
    ```
    
- VideoCapturer.yaml
    
    ```yaml
    # video-generator-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: video-capturer
    spec: # Configuracion del deployment
      replicas: 1 # Indica el número deseado de réplicas del conjunto de pods que el Deployment debe mantener en funcionamiento en todo momento.
      selector: # Especifica cómo el Deployment encuentra qué pods administrar. 
        matchLabels: # Define las etiquetas que deben coincidir con las etiquetas de los pods para que sean seleccionados por este Deployment. 
          app: video-capturer
      template: # Define la plantilla para crear nuevos pods administrados por el Deployment.
        metadata:
          labels: # Especifica las etiquetas que se asignarán a los pods creados por este Deployment.
            app: video-capturer
        spec:
          containers:
          - name: video-capturer # Nombre del contenedor
            volumeMounts:
              - mountPath: /dev/video0
                name: dev-video0
            image: enriquelpzenc/video-capturer_http:latest
            env: # Variables del servicio.
              - name: Feature_Communicator_ip
                value: "192.168.49.2"
              - name: Feature_Communicator_port
                value: "30001"
              - name: Filter_Selector_ip
                value: "192.168.49.2"
              - name: Filter_Selector_port
                value: "30000"
          volumes: # Es una lista de volúmenes que se montarán en el contenedor dentro del Pod.
            - name: dev-video0 # Es el nombre del volumen.
              hostPath: # Especifica que el volumen se montará desde una ruta del sistema de archivos del nodo.
                path: /dev/video0 # Especifica la ruta del sistema de archivos del nodo desde la que se montará el volumen en el contenedor.
    ```
    
- FilterSelector.yaml
    
    ```yaml
    # filter-selector-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: filter-selector
    spec: # Configuracion del deployment
      replicas: 1 # Indica el número deseado de réplicas del conjunto de pods que el Deployment debe mantener en funcionamiento en todo momento.
      selector: # Especifica cómo el Deployment encuentra qué pods administrar. 
        matchLabels: # Define las etiquetas que deben coincidir con las etiquetas de los pods para que sean seleccionados por este Deployment. 
          app: filter-selector
      template: # Define la plantilla para crear nuevos pods administrados por el Deployment.
        metadata:
          labels: # Especifica las etiquetas que se asignarán a los pods creados por este Deployment.
            app: filter-selector
        spec:
          containers:
          - name: filter-selector # Nombre del contenedor
            image: enriquelpzenc/filter_selector_http:latest # Imagen usada para el contenedor.
            ports: # Define los puertos que el contenedor debe exponer.
            - containerPort: 5000 # Especifica el puerto en el que el contenedor escuchará las conexiones entrantes.
            env: # Variables del servicio.
              - name: own_host
                value: "0.0.0.0"
              - name: own_port
                value: "5000"
              - name: Visualizer_ip
                value: "192.168.49.2"
              - name: Visualizer_port
                value: "30003"
    ---
    # service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: filter-selector-service # Nombre que le damos al servicio (solo para identificarlo).
    spec:
      type: LoadBalancer # Tipo de servicio. con loadbalancer, el proveedor se encarga de darle una ip externa. minikube le asigna una para desarrollo local.
      selector:
        app: filter-selector # Define qué pods serán seleccionados por este servicio.
      ports:
        - protocol: TCP # Protocolo habilitado en el puerto.
          port: 5000 # Es el puerto en el que el servicio estará disponible externamente.
          targetPort: 5000 # Es el puerto en el que los pods seleccionados están escuchando.
          nodePort: 30000 # Es el puerto expuesto del nodo en el que el servicio recibirá las solicitudes
          name: "http" # Es el nombre del puerto.
    ---
    ```
    
- FeatureCommunicator.yaml
    
    ```yaml
    # feature-communicator-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: feature-communicator
    spec: # Configuracion del deployment
      replicas: 1 # Indica el número deseado de réplicas del conjunto de pods que el Deployment debe mantener en funcionamiento en todo momento.
      selector: # Especifica cómo el Deployment encuentra qué pods administrar. 
        matchLabels: # Define las etiquetas que deben coincidir con las etiquetas de los pods para que sean seleccionados por este Deployment. 
          app: feature-communicator
      template: # Define la plantilla para crear nuevos pods administrados por el Deployment.
        metadata:
          labels: # Especifica las etiquetas que se asignarán a los pods creados por este Deployment.
            app: feature-communicator
        spec:
          containers:
          - name: feature-communicator # Nombre del contenedor
            image: enriquelpzenc/feature_communicator_http:latest # Imagen usada para el contenedor.
            ports: # Define los puertos que el contenedor debe exponer.
            - containerPort: 5001 # Especifica el puerto en el que el contenedor escuchará las conexiones entrantes.
            env: # Variables del servicio.
              - name: own_host
                value: "0.0.0.0"
              - name: own_port
                value: "5001"
              - name: ArUco_Tracker_ip
                value: "192.168.49.2"
              - name: ArUco_Tracker_port
                value: "30002"
    ---
    # service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: feature-communicator-service # Nombre que le damos al servicio (solo para identificarlo).
    spec:
      type: LoadBalancer # Tipo de servicio. con loadbalancer, el proveedor se encarga de darle una ip externa. minikube le asigna una para desarrollo local.
      selector:
        app: feature-communicator # Define qué pods serán seleccionados por este servicio.
      ports:
        - protocol: TCP # Protocolo habilitado en el puerto.
          port: 5001 # Es el puerto en el que el servicio estará disponible externamente.
          targetPort: 5001 # Es el puerto en el que los pods seleccionados están escuchando.
          nodePort: 30001 # Es el puerto expuesto del nodo en el que el servicio recibirá las solicitudes
          name: "http" # Es el nombre del puerto.
    ---
    ```
    
- ArUcoTracker.yaml
    
    ```yaml
    # aruco-tracker-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: aruco-tracker
    spec: # Configuracion del deployment
      replicas: 1 # Indica el número deseado de réplicas del conjunto de pods que el Deployment debe mantener en funcionamiento en todo momento.
      selector: # Especifica cómo el Deployment encuentra qué pods administrar. 
        matchLabels: # Define las etiquetas que deben coincidir con las etiquetas de los pods para que sean seleccionados por este Deployment. 
          app: aruco-tracker
      template: # Define la plantilla para crear nuevos pods administrados por el Deployment.
        metadata:
          labels: # Especifica las etiquetas que se asignarán a los pods creados por este Deployment.
            app: aruco-tracker
        spec:
          containers:
          - name: aruco-tracker # Nombre del contenedor
            image: enriquelpzenc/aruco_tracker_http:latest # Imagen usada para el contenedor.
            ports: # Define los puertos que el contenedor debe exponer.
            - containerPort: 5002 # Especifica el puerto en el que el contenedor escuchará las conexiones entrantes.
            env:  # Variables del servicio.
              - name: own_host
                value: "0.0.0.0"
              - name: own_port
                value: "5002"
              - name: Visualizer_ip
                value: "192.168.49.2"
              - name: Visualizer_port
                value: "30003"
    ---
    # service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: aruco-tracker-service # Nombre que le damos al servicio (solo para identificarlo).
    spec:
      type: LoadBalancer # Tipo de servicio. con loadbalancer, el proveedor se encarga de darle una ip externa. minikube le asigna una para desarrollo local.
      selector:
        app: aruco-tracker # Define qué pods serán seleccionados por este servicio.
      ports:
        - protocol: TCP # Protocolo habilitado en el puerto.
          port: 5002 # Es el puerto en el que el servicio estará disponible externamente
          targetPort: 5002 # Es el puerto en el que los pods seleccionados están escuchando.
          nodePort: 30002 # Es el puerto expuesto del nodo en el que el servicio recibirá las solicitudes
          name: "http" # Es el nombre del puerto.
    ---
    ```
    
- Visualizer.yaml
    
    ```yaml
    # visualizer-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: visualizer
    spec: # Configuracion del deployment
      replicas: 1 # Indica el número deseado de réplicas del conjunto de pods que el Deployment debe mantener en funcionamiento en todo momento.
      selector: # Especifica cómo el Deployment encuentra qué pods administrar. 
        matchLabels: # Define las etiquetas que deben coincidir con las etiquetas de los pods para que sean seleccionados por este Deployment. 
          app: visualizer
      template: # Define la plantilla para crear nuevos pods administrados por el Deployment.
        metadata:
          labels: # Especifica las etiquetas que se asignarán a los pods creados por este Deployment.
            app: visualizer
        spec:
          containers:
          - name: visualizer # Nombre del contenedor
            image: enriquelpzenc/visualizer_http:latest # Imagen usada para el contenedor.
            ports: # Define los puertos que el contenedor debe exponer.
            - containerPort: 5003 # Especifica el puerto en el que el contenedor escuchará las conexiones entrantes.
            env: # Variables del servicio.
              - name: own_host
                value: "0.0.0.0"
              - name: own_port
                value: "5003"
    ---
    # service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: visualizer-service # Nombre que le damos al servicio (solo para identificarlo).
    spec:
      type: LoadBalancer # Tipo de servicio. con loadbalancer, el proveedor se encarga de darle una ip externa. minikube le asigna una para desarrollo local.
      selector:
        app: visualizer # Define qué pods serán seleccionados por este servicio.
      ports:
        - protocol: TCP # Protocolo habilitado en el puerto.
          port: 5003 # Es el puerto en el que el servicio estará disponible externamente.
          targetPort: 5003 # Es el puerto en el que los pods seleccionados están escuchando.
          nodePort: 30003 # Es el puerto expuesto del nodo en el que el servicio recibirá las solicitudes
          name: "http" # Es el nombre del puerto.
    ---
    
    ```