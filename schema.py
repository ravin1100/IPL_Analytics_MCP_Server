from pydantic import BaseModel


class QuerySchema(BaseModel):
    """Schema for the input query."""

    query: str


class ChatQuery(BaseModel):
    """Schema for the input query."""

    query: str
