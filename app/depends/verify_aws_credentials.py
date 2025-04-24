from app.core.aws_client import textract_client, aws_credentials_valid
from fastapi import HTTPException

async def verify_aws_credentials():
    """Verifica que las credenciales AWS sean válidas."""
    if not textract_client:
        raise HTTPException(
            status_code=500,
            detail="AWS Textract no está configurado. Verifica tus credenciales AWS."
        )
    
    if not aws_credentials_valid:
        raise HTTPException(
            status_code=401,
            detail="Las credenciales AWS no son válidas o han expirado."
        )
    
    return True