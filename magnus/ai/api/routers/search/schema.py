from pydantic import BaseModel


class SearchSchema(BaseModel):
    text: str
    keywords: list[str] = []
