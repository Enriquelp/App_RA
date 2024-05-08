#!/bin/bash

# Lanza todos los microservicios en su versión HTTP

python ./Video_Generator/Video_Generator_http.py &
python ./Filter_Selector/Filter_selector_http.py &
python ./Feature_communicator/Feature_communicator_http.py &
python ./ArUco_tracker/ArUco_tracker_http.py &
python ./Visualizer/Visualizer_http.py &

firefox "http://localhost:5003/visualizer" &
