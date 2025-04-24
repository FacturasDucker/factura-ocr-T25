from typing import Optional
from pydantic import BaseModel
from typing import Optional,Dict,Any
class DebugInfo(BaseModel):
    textract_response: Optional[Dict[str, Any]] = None
    confidence_scores: Optional[Dict[str, float]] = None