import re
def extract_business_name(text: str) -> str:
    """Extrae nombre del negocio de las primeras líneas."""
    lines = text.split('\n')
    
    # find in the first lines
    for i, line in enumerate(lines[:3]):
       
        if (line and len(line) > 3 and 
            not re.search(r'^\d+$', line) and
            not re.search(r'\d{1,2}[/-]\d{1,2}', line) and
            not re.search(r'^\d{1,2}:\d{2}', line) and
            not re.search(r'(?:FOLIO|TICKET|FACTURA)', line, re.IGNORECASE)):
            return line.strip()
    
    return None
