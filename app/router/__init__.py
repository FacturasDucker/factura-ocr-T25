
from fastapi import APIRouter
from app.router.upload_route import router as tickets_router

# Router principal para agrupar todos los endpoints
api_router = APIRouter()

# Incluir todos los routers de la aplicación
api_router.include_router(tickets_router, prefix="/tickets")