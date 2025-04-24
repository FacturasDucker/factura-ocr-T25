import time
from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Depends
from app.core.aws_client import textract_client, aws_credentials_valid
from app.depends.verify_aws_credentials import verify_aws_credentials
from app.models import TicketOCRResponse,TicketData,DebugInfo,TickeResponse
from app.services import  extract_text_with_textract,process_receipt_with_textract
from app.utils import extract_business_name,extract_date_from_text,extract_folio_from_text,extract_total_from_text
import datetime

router = APIRouter(tags=["tickets"])


@router.post(
    "/upload-ticket",
    response_model=TickeResponse,
    summary="Sube una imagen de ticket y extrae datos estructurados usando AWS Textract"
)
async def upload_ticket(
    file: UploadFile = File(...),
    use_analyze_expense: bool = Query(True, description="Usar AnalyzeExpense (más preciso pero más caro)"),
    debug: bool = Query(False, description="Incluir información de debug en la respuesta"),
    credentials_valid: bool = Depends(verify_aws_credentials)
):
    """
    Sube una imagen de ticket y extrae información estructurada usando AWS Textract.
    
    - **file**: Archivo de imagen del ticket (jpg, png, pdf)
    - **use_analyze_expense**: Si es True, usa AnalyzeExpense de Textract (mejor para tickets pero más costoso)
    - **debug**: Si es True, incluye la respuesta completa de Textract en el resultado
    """
    start_time = time.time()
    
    # Verificar tipo de archivo
    if not file.content_type.startswith("image/") and not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen (jpg, png) o PDF"
        )
    
    try:
        # Leer contenido del archivo
        contents = await file.read()
        
        if use_analyze_expense:
            # Usar AnalyzeExpense (específico para recibos)
            parsed_data, raw_text, textract_response, confidence_scores = process_receipt_with_textract(
                contents, debug=debug
            )
        else:
            # Usar DetectDocumentText (más económico)
            raw_text, textract_response = extract_text_with_textract(contents)
            
            # Extraer datos básicos del texto
            parsed_data = TicketData(
                date=extract_date_from_text(raw_text),
                business_name=extract_business_name(raw_text),
                total=extract_total_from_text(raw_text),
                folio=extract_folio_from_text(raw_text)
            )
            confidence_scores = {}
        
        processing_time = time.time() - start_time
        
        # Preparar información de debug
        debug_info = None
        if debug:
            debug_info = DebugInfo(
                textract_response=textract_response,
                confidence_scores=confidence_scores
            )
        ticket_response = TicketOCRResponse(
            raw_text=raw_text,
            parsed=parsed_data,
            processing_time=processing_time,
            debug_info=debug_info
        )

        response_data = {
            "date": ticket_response.parsed.date,
            "folio": ticket_response.parsed.folio
        }

        if ticket_response.parsed.time is not None:
            response_data["time"] = ticket_response.parsed.time

        return TickeResponse(**response_data)
    
    except Exception as e:
        # Capturar y devolver errores específicos de AWS
        error_message = str(e)
        
        if "AccessDeniedException" in error_message:
            raise HTTPException(
                status_code=403,
                detail="Error de acceso a AWS Textract. Verifica tus permisos IAM."
            )
        elif "ResourceNotFoundException" in error_message:
            raise HTTPException(
                status_code=404,
                detail="Recurso no encontrado en AWS Textract."
            )
        elif "ValidationException" in error_message:
            raise HTTPException(
                status_code=400,
                detail=f"Error de validación en AWS Textract: {error_message}"
            )
        elif "ServiceUnavailableException" in error_message:
            raise HTTPException(
                status_code=503,
                detail="AWS Textract no está disponible en este momento. Intenta más tarde."
            )
        elif "ThrottlingException" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Demasiadas solicitudes a AWS Textract. Intenta más tarde."
            )
        elif "UnrecognizedClientException" in error_message:
            raise HTTPException(
                status_code=401,
                detail="Credenciales AWS no reconocidas o expiradas. Actualiza tus credenciales temporales."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar el ticket: {error_message}"
            )