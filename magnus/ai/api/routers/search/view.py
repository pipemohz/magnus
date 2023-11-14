import logging

from fastapi.routing import APIRouter
from ai.api.routers.search.schema import ResultSchema, SearchSchema, RecordSchema

from ai.text_search import search_text, search_keywords
from db import cosmos_client

router = APIRouter()


# @router.post("/", response_model=ResultSchema, openapi_extra={"summary": "Search profiles."})
@router.post("/", openapi_extra={"summary": "Search profiles."})
async def search(search_schema: SearchSchema):
    """
    Search for profiles by text and keywords.
    """

    records = cosmos_client.get().where("IS_DEFINED(container.embedding)").all()

    # text = ",".join([search_schema.text] + search_schema.keywords)
    if len(search_schema.keywords):
        pre_filter = search_keywords(search_schema.keywords, records)
    else:
        pre_filter = None

    text = search_schema.text
    quantity = search_schema.quantity
    similarity = 0.832
    df_results = search_text(text, records, quantity, similarity)

    if pre_filter is not None:
        for _, row in pre_filter.iterrows():
            matching_row = df_results[df_results["id"] == row["id"]]
            if not matching_row.empty:
                df_results.loc[matching_row.index, "similarity"] += row["similarity"]

    records_list = []

    for _, row in df_results.iterrows():
        record_schema = RecordSchema(
            id=row["id"],
            web_url=row["web_url"],
            updated_at=row["updated_at"],
            similarity=row["similarity"],
            filename=row["filename"],
            abstract=row["abstract"],
        )
        records_list.append(record_schema)

    result_schema = ResultSchema(records=records_list)

    # result_schema.records

    return result_schema
