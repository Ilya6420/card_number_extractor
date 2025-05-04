from pydantic import BaseModel


class CardNumberOutput(BaseModel):
    bbox: list[list[int]]
    card_number: str
    confidence: float
