"""
Module to process receipts using AWS Textract AnalyzeExpense
"""
from app.core.aws_client import textract_client
from app.models import TicketData, Item
from app.utils import (
    extract_date_from_text, 
    extract_total_from_text, 
    extract_folio_from_text, 
    extract_business_name
)
from app.services.text_extraction import extract_text_with_textract

def process_receipt_with_textract(file_bytes, debug=False):
    """Procesa un recibo con AWS Textract para extraer campos estructurados."""
    
    # Call the specific API for receipts
    response = textract_client.analyze_expense(
        Document={'Bytes': file_bytes}
    )
    
    # Init data
    parsed_data = TicketData()
    raw_text_lines = []
    confidence_scores = {}
    
    # Process response
    for document in response.get('ExpenseDocuments', []):
        # Extract general fields (date, total, etc.)
        for field in document.get('SummaryFields', []):
            field_type = field.get('Type', {}).get('Text', '').upper()
            
            if 'ValueDetection' in field:
                value = field['ValueDetection'].get('Text', '')
                confidence = field['ValueDetection'].get('Confidence', 0)
                
              
                confidence_scores[field_type] = confidence
                
                
                raw_text_lines.append(f"{field_type}: {value}")
                
                
                if field_type == 'TOTAL' and not parsed_data.total:
                    try:
                        parsed_data.total = float(value.replace('$', '').replace(',', ''))
                    except ValueError:
                        pass
                
                elif field_type == 'SUBTOTAL' and not parsed_data.subtotal:
                    try:
                        parsed_data.subtotal = float(value.replace('$', '').replace(',', ''))
                    except ValueError:
                        pass
                
                elif field_type == 'TAX' and not parsed_data.tax:
                    try:
                        parsed_data.tax = float(value.replace('$', '').replace(',', ''))
                    except ValueError:
                        pass
                
                elif field_type in ['DATE', 'INVOICE_RECEIPT_DATE'] and not parsed_data.date:
                    parsed_data.date = value
                
                elif field_type == 'TIME' and not parsed_data.time:
                    parsed_data.time = value
                
                elif field_type in ['VENDOR_NAME', 'MERCHANT_NAME'] and not parsed_data.business_name:
                    parsed_data.business_name = value
                
                elif field_type in ['RECEIPT_ID', 'INVOICE_RECEIPT_ID'] and not parsed_data.folio:
                    parsed_data.folio = value
                
                elif field_type == 'PAYMENT_METHOD' and not parsed_data.payment_method:
                    parsed_data.payment_method = value
        
        # Extract line items
        items = []
        for group in document.get('LineItemGroups', []):
            for line_item in group.get('LineItems', []):
                item_dict = {}
                
                for field in line_item.get('LineItemExpenseFields', []):
                    field_type = field.get('Type', {}).get('Text', '').upper()
                    
                    if 'ValueDetection' in field:
                        value = field['ValueDetection'].get('Text', '')
                        
                        if field_type == 'ITEM' or field_type == 'DESCRIPTION':
                            item_dict['description'] = value
                        
                        elif field_type == 'PRICE' or field_type == 'TOTAL':
                            try:
                                item_dict['price'] = float(value.replace('$', '').replace(',', ''))
                            except ValueError:
                                item_dict['price'] = 0.0
                        
                        elif field_type == 'QUANTITY':
                            try:
                                item_dict['quantity'] = int(value)
                            except ValueError:
                                try:
                                    # Manejar valores como "1.00"
                                    item_dict['quantity'] = int(float(value))
                                except:
                                    item_dict['quantity'] = 1
                        
                        elif field_type == 'UNIT_PRICE':
                            try:
                                item_dict['unit_price'] = float(value.replace('$', '').replace(',', ''))
                            except ValueError:
                                pass
                
                
                if 'description' in item_dict and 'price' in item_dict:
                    quantity = item_dict.get('quantity', 1)
                    
           
                    unit_price = item_dict.get('unit_price')
                    if not unit_price and quantity > 1 and 'price' in item_dict:
                        unit_price = item_dict['price'] / quantity
                    
                    items.append(Item(
                        quantity=quantity,
                        description=item_dict['description'],
                        price=item_dict['price'],
                        unit_price=unit_price
                    ))
        
        parsed_data.items = items
    

    if not raw_text_lines:

        try:
            general_text, _ = extract_text_with_textract(file_bytes)
            raw_text_lines = general_text.split('\n')
            
            # Try to extract more data of text
            if not parsed_data.date:
                parsed_data.date = extract_date_from_text(general_text)
            
            if not parsed_data.business_name:
                parsed_data.business_name = extract_business_name(general_text)
                
            if not parsed_data.total:
                parsed_data.total = extract_total_from_text(general_text)
                
            if not parsed_data.folio:
                parsed_data.folio = extract_folio_from_text(general_text)
        except Exception as e:
            print(f"Error al extraer texto general: {str(e)}")
    
    raw_text = '\n'.join(raw_text_lines)
    
    return parsed_data, raw_text, response, confidence_scores
