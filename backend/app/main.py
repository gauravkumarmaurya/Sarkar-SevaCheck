import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import admin, auth, ocr, reports, services


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sarkar SevaCheck API",
    version="2.0.0"
)


# CORS
raw_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)

origins = [
    x.strip()
    for x in raw_origins.split(",")
    if x.strip()
]

if "*" in origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# API routers
app.include_router(auth.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(ocr.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


# Frontend build directory
FRONTEND_DIST = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "dist"
)

# Serve frontend assets only when they exist.
# This allows the local backend to run even before `npm run build`.
ASSETS_DIR = FRONTEND_DIST / "assets"

if ASSETS_DIR.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=ASSETS_DIR),
        name="assets"
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "services": "api"
    }


@app.get("/")
def root():
    index = FRONTEND_DIST / "index.html"

    if index.exists():
        return FileResponse(index)

    return {
        "name": "Sarkar SevaCheck API",
        "docs": "/docs",
        "health": "/health"
    }