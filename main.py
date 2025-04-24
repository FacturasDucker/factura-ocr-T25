import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import api_router
from app.core.config import settings

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers
app.include_router(api_router)

@app.get("/")
async def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"message": "Ticket OCR API con AWS Textract está funcionando"}

if __name__ == "__main__":
    # Imprimir información de configuración
    print(f"Inicializando API con región AWS: {settings.AWS_REGION}")
    print(f"Credenciales AWS configuradas: {settings.AWS_ACCESS_KEY_ID is not None}")
    print(f"Token de sesión AWS presente: {settings.AWS_SESSION_TOKEN is not None}")
    
    # Iniciar servidor
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )