rem Lanza todos los microservicios en su version http

@echo off

start python .\Video_Generator\Video_Generator_http.py
start python .\Filter_Selector\Filter_selector_http.py
start python .\Feature_communicator\Feature_communicator_http.py
start python .\ArUco_tracker\ArUco_tracker_http.py
start python .\Visualizer\Visualizer_http.py

start chrome "http://localhost:5003/visualizer"

