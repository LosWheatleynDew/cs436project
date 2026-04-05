@echo off
start "SRV" cmd /k ".venv\Scripts\python.exe" UDPServer.py
start "A" cmd /k ".venv\Scripts\python.exe" UDPClient.py

