@echo off
title MindCare Signal - GenAI & RAG Student Wellness Platform
echo ===================================================================
echo   Starting MindCare Signal (GenAI + RAG + SHAP + ML)
echo   Local Address: http://127.0.0.1:8000
echo   Swagger Docs:  http://127.0.0.1:8000/docs
echo ===================================================================

if exist .venv\Scripts\python.exe (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

%PYTHON_EXE% main.py
pause
