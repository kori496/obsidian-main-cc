@echo off
rem Lanzador de ATKHUB: atkhub <comando>
cd /d "%~dp0"
python -m atkhub %*
