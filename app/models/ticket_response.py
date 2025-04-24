from typing import Optional
from pydantic import BaseModel
from app.models.ticketData import TicketData
from app.models.debugInfo import DebugInfo

class TicketOCRResponse(BaseModel):
    raw_text: str
    parsed: TicketData
    processing_time: float = 0.0
    debug_info: Optional[DebugInfo] = None

    
