import os
import uuid

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport


load_dotenv(".env.test", override=True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def app():
    from app.main import app
    from app.infrastructure.database.prisma_client import connect_db, disconnect_db

    await connect_db()

    yield app

    await disconnect_db()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as async_client:
        yield async_client


@pytest.fixture
def unique_email():
    return f"user_{uuid.uuid4().hex[:8]}@test.com"


@pytest.fixture
async def create_user_and_login(client):
    async def _create_user_and_login(
        email: str | None = None,
        password: str = "123456",
        name: str = "Test User"
    ):
        email = email or f"user_{uuid.uuid4().hex[:8]}@test.com"

        register_response = await client.post(
            "/auth/register",
            json={
                "email": email,
                "password": password,
                "name": name
            }
        )

        assert register_response.status_code in [200, 201]

        login_response = await client.post(
            "/auth/login",
            data={
                "username": email,
                "password": password
            }
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        return {
            "email": email,
            "password": password,
            "token": token,
            "headers": {
                "Authorization": f"Bearer {token}"
            },
            "user": register_response.json()
        }

    return _create_user_and_login


@pytest.fixture
async def create_project(client, create_user_and_login):
    async def _create_project(auth=None):
        auth = auth or await create_user_and_login()

        response = await client.post(
            "/projects/",
            headers=auth["headers"],
            json={
                "name": "Projeto Teste",
                "description": "Projeto criado em teste automatizado",
                "isPublic": False,
                "logoUrl": None,
                "themeColor": "#3B82F6"
            }
        )

        assert response.status_code == 201

        return {
            "auth": auth,
            "project": response.json()
        }

    return _create_project


@pytest.fixture
async def create_form(client, create_project):
    async def _create_form(project_data=None, is_public=False):
        project_data = project_data or await create_project()
        project = project_data["project"]
        auth = project_data["auth"]

        response = await client.post(
            "/forms/",
            headers=auth["headers"],
            json={
                "title": "Formulário Teste",
                "description": "Formulário criado em teste",
                "isPublic": is_public,
                "projectId": project["id"],
                "structure": [
                    {
                        "fieldId": "nome",
                        "label": "Nome",
                        "type": "text",
                        "required": True,
                        "options": []
                    },
                    {
                        "fieldId": "idade",
                        "label": "Idade",
                        "type": "number",
                        "required": True,
                        "options": []
                    },
                    {
                        "fieldId": "curso",
                        "label": "Curso",
                        "type": "select",
                        "required": True,
                        "options": ["ADS", "Logística"]
                    }
                ]
            }
        )

        assert response.status_code == 201

        return {
            "auth": auth,
            "project": project,
            "form": response.json()
        }

    return _create_form