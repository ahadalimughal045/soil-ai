#!/usr/bin/env bash
# Run Project (bash)
# Usage: ./run_project.sh
# - creates .venv
# - activates it
# - installs backend/requirements.txt
# - launches backend/app.py on port 8000

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
  echo "ERROR: Python is not installed or not in PATH. Install Python 3.8+ and retry." >&2
  exit 1
fi

PYTHON=$(command -v python3 || command -v python)

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at $VENV_DIR"
  "$PYTHON" -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

REQ="$ROOT_DIR/backend/requirements.txt"
if [ -f "$REQ" ]; then
  echo "Installing requirements..."
  python -m pip install --upgrade pip
  python -m pip install -r "$REQ"
else
  echo "No requirements.txt found at backend/requirements.txt, skipping install."
fi

echo "Starting Flask backend (backend/app.py) on http://localhost:8000"
"$PYTHON" "$ROOT_DIR/backend/app.py" &
SERVER_PID=$!

sleep 1
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "http://localhost:8000" || true
elif command -v open >/dev/null 2>&1; then
  open "http://localhost:8000" || true
else
  echo "Open http://localhost:8000 in your browser to view the app."
fi

wait $SERVER_PID
