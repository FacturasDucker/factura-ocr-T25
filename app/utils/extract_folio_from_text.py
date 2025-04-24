import re
def extract_folio_from_text(text: str) -> str:
    """Extract number of folio"""
    patterns = [
        r'(?:FOLIO|TICKET|NO)[\.:\s#]*([A-Z0-9]+)',
        r'(?:FACTURA|RECIBO)[\.:\s#]*([A-Z0-9]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None
