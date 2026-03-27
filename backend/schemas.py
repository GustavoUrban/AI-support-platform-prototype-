from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    message: str = Field(..., min_length=5, max_length=5000)


class SearchResult(BaseModel):
    id: int
    message: str
    categoria: str
    score: float
