from fastapi.routing import APIRouter
from ai.api.routers.search.schema import SearchSchema, ResultSchema

from ai.text_search import search_text

router = APIRouter()


@router.post("/", openapi_extra={"summary": "Search profiles."})
def search(search_schema: SearchSchema):
    """
    Search for profiles by text and keywords.
    """

    text = ",".join([search_schema.text] + search_schema.keywords)
    results = search_text(text)
    print("results: ", results)

    return {"records": results}
