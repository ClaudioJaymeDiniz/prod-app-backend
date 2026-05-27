from fastapi import APIRouter


router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    return {
        "status": "online",
        "message": "Smart Forms API - Sistema de Formulários Inteligentes",
        "docs": "/docs",
    }


@router.get("/health")
async def health_check():
    return {
        "status": "ok"
    }