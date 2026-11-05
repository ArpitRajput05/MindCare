@echo off
echo ==================================================
echo   Starting Mental Health Score Web Application
echo ==================================================

if exist .venv\Scripts\python.exe (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo Starting server at http://127.0.0.1:8000 ...
%PYTHON_EXE% main.py
pause
