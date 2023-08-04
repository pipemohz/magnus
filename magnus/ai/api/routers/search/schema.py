from pydantic import BaseModel


class SearchSchema(BaseModel):
    text: str
    keywords: list[str] = []
    quantity: int


class RecordSchema(BaseModel):
    id: str
    web_url: str
    updated_at: str
    similarity: float


class ResultSchema(BaseModel):
    records: list[RecordSchema]
