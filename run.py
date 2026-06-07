# import uvicorn

# from app.core.config import settings


# if __name__ == "__main__":
#     print(f"🚀 Iniciando servidor em http://{settings.HOST}:{settings.PORT}")

#     uvicorn.run(
#         "app.main:app",
#         host=settings.HOST,
#         port=settings.PORT,
#         reload=True,
#         reload_excludes=[
#             "venv/*",
#             "**/__pycache__/*",
#             "prisma/*"
#         ],
#     )


import uvicorn
import ngrok
import asyncio
from dotenv import load_dotenv 
from app.core.config import settings

# 2. Carrega as variáveis do .env (incluindo o NGROK_AUTHTOKEN) antes de tudo
load_dotenv()

async def setup_ngrok():
    try:
        # Agora o authtoken_from_env=True vai encontrar a chave perfeitamente
        listener = await ngrok.forward(settings.PORT, authtoken_from_env=True)
        print(f"\n🔗 [Ngrok] Seu túnel público está ativo!")
        print(f"🔗 URL para colocar no seu Expo: {listener.url()}\n")
    except Exception as e:
        print(f"⚠️ Não foi possível iniciar o Ngrok automaticamente: {e}")
        print("Certifique-se de que o NGROK_AUTHTOKEN está configurado.\n")

if __name__ == "__main__":
    # Inicia o Ngrok de forma assíncrona antes do Uvicorn barrar o terminal
    asyncio.run(setup_ngrok())

    print(f"🚀 Iniciando servidor local em http://{settings.HOST}:{settings.PORT}")

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