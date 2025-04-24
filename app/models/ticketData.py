from typing import Optional
from pydantic import BaseModel,Field
from typing import Optional, List
from app.models.item import Item

class TicketData(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    total: Optional[float] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    items: List[Item] = Field(default_factory=list)
    business_name: Optional[str] = None
    order_number: Optional[str] = None
    folio: Optional[str] = None
    payment_method: Optional[str] = None