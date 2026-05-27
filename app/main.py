from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.cors import setup_cors
from app.core.exception_handlers import app_exception_handler
from app.core.exceptions import AppException
from app.infrastructure.database.prisma_client import connect_db, disconnect_db

from app.features.health.routes import router as health_router
from app.features.auth.routes import router as auth_router
from app.features.projects.routes import router as projects_router
from app.features.invitations.routes import router as invitations_router
from app.features.forms.routes import router as forms_router
from app.features.uploads.routes import router as uploads_router
from app.features.submissions.routes import router as submissions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    print("🚀 API iniciada e banco conectado.")

    yield

    await disconnect_db()
    print("🛑 Conexão com o banco encerrada.")


app = FastAPI(
    lifespan=lifespan,
    title="Smart Forms API",
    description="Backend para gestão de formulários dinâmicos com sincronização offline e analytics.",
    version="1.0.0",
    contact={
        "name": "Claudio Jayme",
        "url": "https://github.com/ClaudioJaymeDiniz",
    },
)

app.add_exception_handler(AppException, app_exception_handler)

setup_cors(app)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(invitations_router)
app.include_router(forms_router)
app.include_router(uploads_router)
app.include_router(submissions_router)