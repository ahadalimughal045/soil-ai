<#
Run Project (PowerShell)

Usage:
  .\run_project.ps1         # runs interactively

What it does:
  - Creates a virtual environment in .venv
  - Activates it
  - Installs dependencies from backend/requirements.txt
  - Launches the Flask backend (backend/app.py) on port 8000
  - Opens http://localhost:8000 in the default browser
#>
Set-StrictMode -Version Latest

function Abort([string]$msg){
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Abort "Python is not found in PATH. Install Python 3.8+ and re-run this script."
}

$venvPath = Join-Path $PSScriptRoot '.venv'

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath..."
    python -m venv $venvPath || Abort "Failed to create virtual environment."
}

Write-Host "Activating virtual environment..."
& "$venvPath\Scripts\Activate.ps1"

$req = Join-Path $PSScriptRoot 'backend\requirements.txt'
if (Test-Path $req) {
    Write-Host "Installing requirements... (this may take a while)"
    python -m pip install --upgrade pip
    python -m pip install -r $req
} else {
    Write-Host "No requirements.txt found at backend/requirements.txt, skipping install."
}

Write-Host "Starting Flask backend (backend/app.py) on http://localhost:8000"
Start-Process -FilePath python -ArgumentList 'backend/app.py'

try {
    Start-Process 'http://localhost:8000'
} catch {
    Write-Host "Open http://localhost:8000 in your browser to view the app."
}

Write-Host "Server launched. Use Ctrl+C in the backend process or stop the python process to stop the server."
