from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import (
    Base,
    engine
)

from routers.auth import router as auth_router
from routers.interview import router as interview_router
from routers.report import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    print("InterviewPilot Backend Started")

    yield

    print("InterviewPilot Backend Stopped")


app = FastAPI(
    title="InterviewPilot API",
    description="AI Powered Mock Interview Platform",
    version="1.0.0",
    lifespan=lifespan
)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    interview_router,
    prefix="/interview",
    tags=["Interview"]
)

app.include_router(
    report_router,
    prefix="/report",
    tags=["Reports"]
)


@app.get("/")
def root():
    return {
        "application": "InterviewPilot",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }