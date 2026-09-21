# Sarkar SevaCheck — Final Demo Build

Full-stack hackathon demo for transparent government-service fee guidance.

## Included
- 20 service records: 2 official verified + 18 clearly labelled synthetic demo/test records
- Responsive React/Vite UI
- FastAPI API + SQLite
- Mobile demo login/register with JWT
- Receipt OCR using Tesseract
- OCR amount comparison and evidence report
- My Reports
- Admin panel: stats, create, edit, delete
- OpenStreetMap/Leaflet district map
- Hindi/English toggle
- Docker deployment for a single public web service

## Demo accounts
- Citizen: `9876543210`
- Admin: `9999999999`

The login is intentionally passwordless for hackathon demonstration. It is not production authentication.

## Windows local run
### Backend
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m app.seed
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### Frontend (second PowerShell)
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173`.

## OCR on Windows
Install Tesseract OCR. The backend automatically checks the standard path `C:\Program Files\Tesseract-OCR\tesseract.exe`. Or set `TESSERACT_CMD`.

## Deployment
The included `Dockerfile` builds the React app and serves it through FastAPI. It is designed for a Render Docker Web Service. Render requires the service to listen on `0.0.0.0`; the included image uses `${PORT:-10000}`.

For a public deployment, set a strong `SECRET_KEY` and use PostgreSQL rather than ephemeral SQLite for persistent production data.

## Data accuracy
Only Caste Certificate and Employment Registration are labelled official verified in the demo. The other 18 amounts are synthetic hackathon test values and must not be presented as government fees.
