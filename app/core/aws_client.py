import boto3
from app.core.config import settings

def test_aws_credentials():
    """Prueba las credenciales AWS para verificar que son válidas."""
    try:
        # Intenta una operación simple
        sts = boto3.client(
            'sts',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_REGION
        )
        
        response = sts.get_caller_identity()
        print(f"✅ Credenciales AWS válidas para: {response.get('Arn')}")
        expiry = response.get('Expiration', 'No disponible')
        if expiry != 'No disponible':
            print(f"Expiran: {expiry}")
        return True
    except Exception as e:
        print(f"❌ Error de credenciales AWS: {str(e)}")
        return False

def create_textract_client():
    """Crea y configura un cliente de AWS Textract."""
    try:
        # Crear cliente con credenciales específicas si están disponibles
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            client = boto3.client(
                'textract',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=settings.AWS_SESSION_TOKEN,  # Puede ser None
                region_name=settings.AWS_REGION
            )
    
            print("Cliente AWS Textract inicializado con credenciales explícitas")
        else:
            # Usar configuración de ~/.aws/ si no hay credenciales en .env
            client = boto3.client('textract', region_name=settings.AWS_REGION)
            print("Cliente AWS Textract inicializado con credenciales desde ~/.aws/ o roles IAM")
        
        return client
    except Exception as e:
        print(f"Error al configurar AWS Textract: {str(e)}")
        return None

# Inicializar cliente y verificar credenciales
textract_client = create_textract_client()
aws_credentials_valid = test_aws_credentials()