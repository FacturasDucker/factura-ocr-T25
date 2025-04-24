from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class TickeResponse(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = datetime.now().strftime('%H:%M:%S')
    folio: Optional[str] = None
    payment_method: Optional[str] = None

    @field_validator('time', mode='before')
    @classmethod
    def set_default_time(cls, value):
        return value or datetime.now().strftime('%H:%M:%S')
