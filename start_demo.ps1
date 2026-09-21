$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "[1/3] Backend setup..." -ForegroundColor Cyan
Set-Location "$Root\backend"
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    py -m venv .venv
}
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m app.seed

Write-Host "[2/3] Starting FastAPI..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList '-NoExit','-Command',"Set-Location '$Root\backend'; .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

Write-Host "[3/3] Start frontend in a new terminal with:" -ForegroundColor Cyan
Write-Host "cd `"$Root\frontend`"; npm install; npm run dev" -ForegroundColor Yellow
Write-Host "Open http://localhost:5173" -ForegroundColor Green
