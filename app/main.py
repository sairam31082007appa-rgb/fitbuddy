from pathlib import Path

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.database import init_db

from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent


app = FastAPI(

    title="FitBuddy AI Fitness Planner",

    description=(
        "AI-powered personalized fitness "
        "plan generator."
    ),

    version="1.0.0"
)


# Static files
app.mount(

    "/static",

    StaticFiles(
        directory=BASE_DIR / "static"
    ),

    name="static"
)


# Routes
app.include_router(
    router
)


# Database initialization
@app.on_event("startup")
def startup():

    init_db()


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "application": "FitBuddy"
    }