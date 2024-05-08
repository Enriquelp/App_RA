#!/bin/bash

# Lanza todos los microservicios en su versión socket

python ./Video_Generator/Video_Generator.py &
python ./Filter_Selector/Filter_selector.py &
python ./Feature_communicator/Feature_communicator.py &
python ./ArUco_tracker/ArUco_tracker.py &
python ./Visualizer/Visualizer.py &

firefox "http://localhost:5003/visualizer" &
