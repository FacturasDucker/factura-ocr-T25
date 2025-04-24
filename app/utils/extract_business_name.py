import re
def extract_business_name(text: str) -> str:
    """Extrae nombre del negocio de las primeras líneas."""
    lines = text.split('\n')
    
    # Buscar en las primeras líneas
    for i, line in enumerate(lines[:3]):
        # Ignorar líneas que sean claramente no nombres de negocio
        if (line and len(line) > 3 and 
            not re.search(r'^\d+$', line) and
            not re.search(r'\d{1,2}[/-]\d{1,2}', line) and
            not re.search(r'^\d{1,2}:\d{2}', line) and
            not re.search(r'(?:FOLIO|TICKET|FACTURA)', line, re.IGNORECASE)):
            return line.strip()
    
    return None