import logging

from fastapi.routing import APIRouter
from ai.api.routers.search.schema import ResultSchema, SearchSchema, RecordSchema

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
    records_list = []

    for _, row in results.iterrows():
        record_schema = RecordSchema(
            id=row['id'],
            web_url=row['web_url'],
            updated_at=row['updated_at'],
            similarity=row['similarity'],
            filename=row['filename'],
            abstract=row['abstract']
        )
        records_list.append(record_schema)

    result_schema = ResultSchema(records=records_list)

    # result_schema.records
    logging.warning(result_schema)

    return result_schema
