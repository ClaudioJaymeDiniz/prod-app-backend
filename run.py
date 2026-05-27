import uvicorn

from app.core.config import settings


if __name__ == "__main__":
    print(f"🚀 Iniciando servidor em http://{settings.HOST}:{settings.PORT}")

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        reload_excludes=[
            "venv/*",
            "**/__pycache__/*",
            "prisma/*"
        ],
    )