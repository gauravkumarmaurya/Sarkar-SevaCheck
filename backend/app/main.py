import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .database import Base, engine
from .routers import admin, auth, ocr, reports, services

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sarkar SevaCheck API", version="2.0.0")

raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [x.strip() for x in raw_origins.split(",") if x.strip()]
if "*" in origins:
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
else:
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(ocr.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok", "services": "api"}


@app.get("/")
def root():
    index = Path(__file__).resolve().parents[2] / "frontend" / "dist" / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"name": "Sarkar SevaCheck API", "docs": "/docs", "health": "/health"}
