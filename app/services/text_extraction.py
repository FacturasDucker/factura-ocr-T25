from app.core.aws_client import textract_client
from app.models import TicketData,Item


def extract_text_with_textract(file_bytes):
    """Extracts plain text from a document using AWS Textract DetectDocumentText."""
    response = textract_client.detect_document_text(
        Document={'Bytes': file_bytes}
    )
    
    # Extracts text
    text_lines = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text_lines.append(item['Text'])
    
    full_text = '\n'.join(text_lines)
    return full_text, response
