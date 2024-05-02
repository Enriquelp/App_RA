rem Lanza todos los microservicios en su version socket

@echo off

start python .\Video_Generator\Video_Generator.py
start python .\Filter_Selector\Filter_selector.py
start python .\Feature_communicator\Feature_communicator.py
start python .\ArUco_tracker\ArUco_tracker.py
start python .\Visualizer\Visualizer.py
