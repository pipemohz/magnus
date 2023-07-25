import logging

from fastapi.routing import APIRouter
from ai.api.routers.search.schema import SearchSchema

from ai.text_search import search_text

router = APIRouter()


@router.post(
    "/", response_model=SearchSchema, openapi_extra={"summary": "Search profiles."}
)
def search(search_schema: SearchSchema):
    """
    Search for profiles by text and keywords.
    """

    logging.info(search_text(search_schema.text))

    return search_schema
