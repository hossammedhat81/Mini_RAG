from fastapi import FastAPI , APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",  # Set a global prefix for all routes
    tags=["api_v1"],  # Add tags for API documentation
)


@base_router.get("/")        #decorator required to tell FastAPI that the function immediately below is in charge of handling requests that go to the path "/welcome" using the GET HTTP method.
def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "app_name": app_name,
        "app_version": app_version,
        "message":"Hello All, welcome to the Mini RAG application!"
    }

