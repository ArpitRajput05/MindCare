@echo off
echo ==================================================
echo   MindCare - Mental Health Score Web App
echo   Powered by FastAPI & Scikit-Learn
echo ==================================================

if exist .venv\Scripts\python.exe (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo Starting backend server on http://127.0.0.1:8000 ...
echo Interactive Swagger Docs at http://127.0.0.1:8000/docs
echo.

%PYTHON_EXE% main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Server stopped with error code %ERRORLEVEL%.
    pause
)
