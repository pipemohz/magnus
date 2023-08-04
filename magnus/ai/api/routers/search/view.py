import logging

from fastapi.routing import APIRouter
from ai.api.routers.search.schema import ResultSchema, SearchSchema

from ai.text_search import search_text

router = APIRouter()


# @router.post("/", response_model=ResultSchema, openapi_extra={"summary": "Search profiles."})
@router.post("/", openapi_extra={"summary": "Search profiles."})
def search(search_schema: SearchSchema):
    """
    Search for profiles by text and keywords.
    """

    text = ",".join([search_schema.text] + search_schema.keywords)
    n = search_schema.quantity
    results = search_text(text, n)

    logging.warning(results)

    return {"records": results}
