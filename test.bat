@echo off
start "SRV" cmd /k ".venv\Scripts\python.exe" UDPServer.py
timeout /t 0.1
start "A" cmd /k ".venv\Scripts\python.exe" UDPClient.py


