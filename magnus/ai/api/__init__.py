from fastapi import FastAPI
from fastapi.routing import APIRouter

metadata = [
    {
        "name": "meta",
        "description": "Services for checking API status.",
    },
    {
        "name": "search",
        "description": "Services for searching job profiles.",
    },
]


def create_app():
    app = FastAPI(
        title="Magnus AI API",
        version="v1",
        docs_url="/ai/api/docs",
        redoc_url="/ai/api/redoc",
        openapi_url="/ai/api/openapi.json",
        openapi_tags=metadata,
    )

    router = APIRouter(prefix="/ai/api")

    from ai.api import main
    from ai.api.routers import search

    router.include_router(main.router, tags=["meta"])
    router.include_router(search.router, prefix="/search", tags=["search"])

    app.include_router(router)

    return app
