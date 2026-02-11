#!/usr/bin/env python3
"""
run_all.py

Starts both the backend Flask app and a static server for the frontend in one command.

Usage:
  python run_all.py

Behavior:
  - Ensures a virtual environment at .venv
  - Installs requirements from backend/requirements.txt (if present)
  - Launches backend/app.py using the venv Python
  - Serves frontend/ on port 3000 using the venv Python's http.server
  - Opens the frontend in the default browser
  - Cleans up child processes on Ctrl+C
"""
import os
import sys
import subprocess
import shutil
import signal
import time
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(ROOT, ".venv")
REQ_FILE = os.path.join(ROOT, "backend", "requirements.txt")


def python_in_path():
    for name in ("python3", "python"):
        path = shutil.which(name)
        if path:
            return path
    return None


def venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def ensure_venv():
    py = python_in_path()
    if not py:
        print("ERROR: Python not found in PATH. Install Python 3.8+ and retry.")
        sys.exit(1)

    if not os.path.isdir(VENV_DIR):
        print("Creating virtual environment at .venv...")
        subprocess.check_call([py, "-m", "venv", VENV_DIR])

    vp = venv_python()
    if not os.path.exists(vp):
        print("ERROR: venv python not found at", vp)
        sys.exit(1)
    return vp


def install_requirements(python_exec):
    if os.path.exists(REQ_FILE):
        print("Installing requirements from backend/requirements.txt (may take several minutes)...")
        subprocess.check_call([python_exec, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([python_exec, "-m", "pip", "install", "-r", REQ_FILE])
    else:
        print("No requirements file found at backend/requirements.txt — skipping install.")


def start_processes(python_exec):
    procs = []

    # Start backend
    backend_script = os.path.join(ROOT, "backend", "app.py")
    if not os.path.exists(backend_script):
        print(f"ERROR: backend script not found at {backend_script}")
        sys.exit(1)

    print("Starting backend: python backend/app.py (port 8000)")
    p_backend = subprocess.Popen([python_exec, backend_script], cwd=ROOT)
    procs.append(("backend", p_backend))

    # Start frontend static server on port 3000
    print("Starting frontend static server on http://localhost:3000/")
    p_frontend = subprocess.Popen([python_exec, "-m", "http.server", "3000", "--directory", os.path.join(ROOT, "frontend")], cwd=ROOT)
    procs.append(("frontend", p_frontend))

    # Give servers a moment to boot
    time.sleep(1.5)

    # Open browser to frontend index
    try:
        webbrowser.open("http://localhost:3000/index.html")
    except Exception:
        print("Open http://localhost:3000/index.html in your browser to view the app.")

    return procs


def stop_processes(procs):
    for name, p in procs:
        try:
            print(f"Stopping {name} (pid={p.pid})")
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    p.kill()
        except Exception as e:
            print(f"Error stopping {name}: {e}")


def main():
    vp = ensure_venv()
    install_requirements(vp)

    procs = start_processes(vp)

    def handle_sigint(sig, frame):
        print("\nReceived interrupt — stopping child processes...")
        stop_processes(procs)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    # Wait for child processes — if any exits, stop the others
    try:
        while True:
            for name, p in list(procs):
                ret = p.poll()
                if ret is not None:
                    print(f"{name} exited with code {ret}. Shutting down remaining processes.")
                    stop_processes([x for x in procs if x[1] != p])
                    sys.exit(ret)
            time.sleep(0.5)
    except KeyboardInterrupt:
        handle_sigint(None, None)


if __name__ == "__main__":
    main()
