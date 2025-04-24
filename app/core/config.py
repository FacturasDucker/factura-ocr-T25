import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

#
load_dotenv()

class Settings:
    # API Config
    API_TITLE: str = "Ticket OCR API con AWS Textract"
    API_DESCRIPTION: str = "Procesa tickets y extrae datos estructurados usando AWS Textract"
    API_VERSION: str = "1.0.0"
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID: Optional[str] = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN: Optional[str] = os.environ.get("AWS_SESSION_TOKEN")
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-west-2")
    
    # App Settings
    PORT: int = int(os.environ.get("PORT", 5000))
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() == "true"
    
    # Validar configuración
    def validate(self) -> bool:
        """Valida que la configuración mínima esté presente."""
        required_keys = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
        for key in required_keys:
            if not getattr(self, key):
                print(f"⚠️ Advertencia: La variable de entorno {key} no está configurada")
                return False
        return True
    
    def __str__(self) -> str:
        """Representación en cadena segura (sin credenciales)."""
        return (
            f"Settings(API_VERSION={self.API_VERSION}, "
            f"AWS_REGION={self.AWS_REGION}, "
            f"AWS_CREDENTIALS_CONFIGURED={'Sí' if self.AWS_ACCESS_KEY_ID else 'No'}, "
            f"DEBUG={self.DEBUG})"
        )

# Instancia de configuración para usar en toda la aplicación
settings = Settings()
