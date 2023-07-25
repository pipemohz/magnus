from fastapi.routing import APIRouter
from ai.api.routers.search.schema import SearchSchema

router = APIRouter()


@router.post(
    "/", response_model=SearchSchema, openapi_extra={"summary": "Search profiles."}
)
def search(search_schema: SearchSchema):
    """
    Search for profiles by text and keywords.
    """

    return search_schema
