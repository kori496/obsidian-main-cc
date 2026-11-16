@echo off
rem Abre la interfaz grafica de ATKHUB (doble clic)
cd /d "%~dp0"
start "" pythonw -m atkhub gui
