from typing import Optional
from pydantic import BaseModel
class Item(BaseModel):
    quantity: int = 1
    description: str
    price: float
    unit_price: Optional[float] = None