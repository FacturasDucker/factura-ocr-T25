# Importaciones desde archivos separados
from app.services.text_extraction import extract_text_with_textract
from app.services.process_receipt_with_textract import process_receipt_with_textract

# Exportar funciones
__all__ = ["extract_text_with_textract", "process_receipt_with_textract"]