"""
MindCare Signal - Entry Point
Main entrypoint for local execution and backwards compatibility.
Imports the modular application from app.main.
"""

import sys
import os
import webbrowser
import threading
import uvicorn

# Ensure repository root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.main import app  # noqa: E402


def open_browser():
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    print("==================================================")
    print("  Starting MindCare Signal (GenAI + RAG + ML)     ")
    print("  URL: http://127.0.0.1:8000                     ")
    print("  Docs: http://127.0.0.1:8000/docs               ")
    print("==================================================")

    # Automatically open the web browser when the server starts in local mode
    if os.environ.get("OPEN_BROWSER", "true").lower() in ("true", "1"):
        threading.Timer(1.5, open_browser).start()

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
