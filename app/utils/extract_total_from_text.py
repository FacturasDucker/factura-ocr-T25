import re
def extract_total_from_text(text: str) -> float:
    """Extrae el total del texto."""
    patterns = [
        r'(?:TOTAL)[:\s]*\$?\s*(\d+[.,]\d{2})',
        r'(?:TOTAL|IMPORTE)[:\s]*MXN\s*(\d+[.,]\d{2})',
        r'(?:TOTAL|IMPORTE)[:\s]*(?:MX\$|MX)\s*(\d+[.,]\d{2})'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            try:
                return float(matches[-1].replace(',', '.'))
            except ValueError:
                pass
    
    return None