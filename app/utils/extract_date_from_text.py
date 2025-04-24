import re

def extract_date_from_text(text: str) -> str:
    """Extrae fecha de un texto."""
    patterns = [
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # dd/mm/yyyy o dd-mm-yyyy
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',    # yyyy/mm/dd o yyyy-mm-dd
        r'(?:FECHA|DATE)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'  # FECHA: dd/mm/yyyy
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0]
    
    return None