import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from prisma import Json

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.infrastructure.database.prisma_client import db
from app.infrastructure.security.password_service import hash_password


OWNER_ID = "0f3589d0-8c08-4efb-a657-db28e4e31e9c"
OWNER_EMAIL = "claudiojayme@gmail.com"
OWNER_PASSWORD = "102030"

PROJECT_ID = "d1a60ecc-a732-4aa2-9544-759b65c17617"
PROJECT_NAME = "Fatec"
PROJECT_COLOR = "#8B5CF6"

FORM_ID = "4fd2947e-4fc4-43a1-b29a-1df536c434c6"
FORM_TITLE = "Avaliação Fatec"
FORM_DESCRIPTION = "Avaliação dos cursos da Fatec."

RESPONDENTS = [
    {"name": "Ana", "email": "ana@teste.com", "password": "102030"},
    {"name": "Bruno", "email": "bruno@teste.com", "password": "102030"},
    {"name": "Cassia", "email": "cassia@teste.com", "password": "102030"},
    {"name": "Diego", "email": "diego@teste.com", "password": "102030"},
]

FORM_STRUCTURE = [
    {
        "type": "text",
        "label": "Nome completo",
        "fieldId": "nome_completo",
        "options": None,
        "required": True,
    },
    {
        "type": "number",
        "label": "Idade",
        "fieldId": "idade",
        "options": None,
        "required": True,
    },
    {
        "type": "select",
        "label": "Curso",
        "fieldId": "curso",
        "options": ["ADS", "Logística", "DSM", "RH"],
        "required": True,
    },
    {
        "type": "checkbox",
        "label": "Quais laboratórios vc utiliza?",
        "fieldId": "quais_laboratorios_vc_utiliza",
        "options": ["Informática", "Redes", "Eletrônica", "Hardware"],
        "required": True,
    },
    {
        "type": "select",
        "label": "Avaliação geral",
        "fieldId": "avaliacao_geral",
        "options": ["Excelente", "Boa", "Regular", "Ruim"],
        "required": True,
    },
    {
        "type": "textarea",
        "label": "Comentários ",
        "fieldId": "comentarios",
        "options": None,
        "required": True,
    },
    {
        "type": "image",
        "label": "Foto do ambiente",
        "fieldId": "foto_do_ambiente",
        "options": None,
        "required": False,
    },
]

COURSES = ["ADS", "Logística", "DSM", "RH"]
RATINGS = ["Excelente", "Boa", "Regular", "Ruim"]
LABS = [
    ["Informática"],
    ["Informática", "Redes"],
    ["Redes", "Hardware"],
    ["Informática", "Eletrônica"],
    ["Informática", "Redes", "Hardware"],
    ["Eletrônica"],
]
COMMENTS = [
    "Os laboratórios ajudam bastante nas aulas práticas.",
    "A estrutura atende bem, mas alguns computadores poderiam ser atualizados.",
    "Gostei da organização do curso neste semestre.",
    "Seria bom ter mais horários disponíveis para uso dos laboratórios.",
    "As salas estão adequadas e os professores são atenciosos.",
    "A internet oscila em alguns momentos durante as aulas.",
    "O ambiente é bom para estudar e fazer projetos em grupo.",
    "Alguns equipamentos precisam de manutenção preventiva.",
    "A experiência geral tem sido positiva.",
    "A sinalização e a disponibilidade dos espaços poderiam melhorar.",
]


async def upsert_user(email: str, name: str, password: str, user_id: str | None = None):
    create_data = {
        "email": email,
        "name": name,
        "password": hash_password(password),
        "provider": "local",
        "globalMetadata": Json({}),
    }

    if user_id:
        create_data["id"] = user_id

    return await db.user.upsert(
        where={"email": email},
        data={
            "create": create_data,
            "update": {
                "name": name,
                "password": hash_password(password),
                "provider": "local",
                "globalMetadata": Json({}),
            },
        },
    )


async def upsert_project_member(user_id: str, project_id: str, role: str):
    await db.userproject.upsert(
        where={
            "userId_projectId": {
                "userId": user_id,
                "projectId": project_id,
            }
        },
        data={
            "create": {
                "userId": user_id,
                "projectId": project_id,
                "role": role,
                "projectSpecificMetadata": Json({}),
            },
            "update": {
                "role": role,
                "projectSpecificMetadata": Json({}),
            },
        },
    )


async def upsert_accepted_invitation(user, project_id: str):
    await db.projectinvitation.upsert(
        where={
            "email_projectId": {
                "email": user.email,
                "projectId": project_id,
            }
        },
        data={
            "create": {
                "email": user.email,
                "projectId": project_id,
                "role": "COLLECTOR",
                "status": "ACCEPTED",
                "userId": user.id,
            },
            "update": {
                "role": "COLLECTOR",
                "status": "ACCEPTED",
                "userId": user.id,
            },
        },
    )


def build_submission_data(user_name: str, answer_index: int, global_index: int):
    return {
        "nome_completo": f"{user_name}",
        "idade": 18 + (global_index % 16),
        "curso": COURSES[global_index % len(COURSES)],
        "quais_laboratorios_vc_utiliza": LABS[global_index % len(LABS)],
        "avaliacao_geral": RATINGS[global_index % len(RATINGS)],
        "comentarios": COMMENTS[global_index % len(COMMENTS)],
    }


async def main():
    await db.connect()

    print("Iniciando seed de respostas da Avaliação Fatec...")

    owner = await upsert_user(
        email=OWNER_EMAIL,
        name="Claudio Jayme",
        password=OWNER_PASSWORD,
        user_id=OWNER_ID,
    )

    project = await db.project.upsert(
        where={"id": PROJECT_ID},
        data={
            "create": {
                "id": PROJECT_ID,
                "name": PROJECT_NAME,
                "description": "Projeto Fatec para avaliações institucionais.",
                "logoUrl": None,
                "themeColor": PROJECT_COLOR,
                "isPublic": True,
                "owner": {"connect": {"id": owner.id}},
            },
            "update": {
                "name": PROJECT_NAME,
                "description": "Projeto Fatec para avaliações institucionais.",
                "themeColor": PROJECT_COLOR,
                "isPublic": True,
                "owner": {"connect": {"id": owner.id}},
                "deletedAt": None,
            },
        },
    )

    await upsert_project_member(owner.id, project.id, "OWNER")

    respondents = []
    for respondent_data in RESPONDENTS:
        respondent = await upsert_user(**respondent_data)
        respondents.append(respondent)

        await upsert_project_member(respondent.id, project.id, "COLLECTOR")
        await upsert_accepted_invitation(respondent, project.id)

    form = await db.form.upsert(
        where={"id": FORM_ID},
        data={
            "create": {
                "id": FORM_ID,
                "title": FORM_TITLE,
                "description": FORM_DESCRIPTION,
                "isPublic": True,
                "structure": Json(FORM_STRUCTURE),
                "project": {"connect": {"id": project.id}},
            },
            "update": {
                "title": FORM_TITLE,
                "description": FORM_DESCRIPTION,
                "isPublic": True,
                "structure": Json(FORM_STRUCTURE),
                "project": {"connect": {"id": project.id}},
                "deletedAt": None,
            },
        },
    )

    await db.submission.delete_many(where={"formId": form.id})

    first_submission_date = datetime(2026, 5, 20, 9, 0, tzinfo=timezone.utc)
    total_created = 0

    for user_index, respondent in enumerate(respondents):
        for answer_index in range(10):
            global_index = user_index * 10 + answer_index
            created_at = (
                first_submission_date
                + timedelta(days=answer_index + user_index * 2)
                + timedelta(hours=(global_index * 3) % 11)
            )

            await db.submission.create(
                data={
                    "id": str(uuid4()),
                    "formData": Json(
                        build_submission_data(
                            respondent.name or respondent.email,
                            answer_index,
                            global_index,
                        )
                    ),
                    "user": {"connect": {"id": respondent.id}},
                    "form": {"connect": {"id": form.id}},
                    "createdAt": created_at,
                }
            )

            total_created += 1

    print("Seed concluído!")
    print(f"Projeto: {project.name} ({project.id})")
    print(f"Formulário: {form.title} ({form.id})")
    print(f"Respostas criadas: {total_created}")
    print("")
    print("Logins dos respondentes:")

    for respondent in RESPONDENTS:
        print(f"- {respondent['name']}: {respondent['email']} / {respondent['password']}")

    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
