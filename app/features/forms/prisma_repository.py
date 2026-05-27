from prisma import Json

from app.infrastructure.database.prisma_client import db
from app.features.forms.repositories import FormRepository


class PrismaFormRepository(FormRepository):

    async def create(self, data: dict):
        return await db.form.create(
            data=data
        )

    async def find_project_by_id(self, project_id: str):
        return await db.project.find_unique(
            where={"id": project_id}
        )

    async def find_by_id(self, form_id: str):
        return await db.form.find_unique(
            where={"id": form_id}
        )

    async def find_by_id_with_project(self, form_id: str):
        return await db.form.find_unique(
            where={"id": form_id},
            include={
                "project": True
            }
        )

    async def find_by_id_with_project_and_submissions(self, form_id: str):
        return await db.form.find_unique(
            where={"id": form_id},
            include={
                "project": True,
                "submissions": {
                    "include": {
                        "user": True
                    }
                }
            }
        )

    async def list_by_project(self, project_id: str):
        return await db.form.find_many(
            where={
                "projectId": project_id,
                "deletedAt": None
            },
            include={
                "submissions": True
            }
        )

    async def list_public(self):
        return await db.form.find_many(
            where={
                "isPublic": True,
                "deletedAt": None
            },
            include={
                "project": True
            },
            order={
                "createdAt": "desc"
            }
        )

    async def update(self, form_id: str, data: dict):
        if "structure" in data and not isinstance(data["structure"], Json):
            data["structure"] = Json(data["structure"])

        return await db.form.update(
            where={"id": form_id},
            data=data
        )

    async def delete_submissions_by_form(self, form_id: str):
        return await db.submission.delete_many(
            where={
                "formId": form_id
            }
        )

    async def delete_permanent(self, form_id: str):
        return await db.form.delete(
            where={
                "id": form_id
            }
        )

    async def list_submissions_by_form(self, form_id: str):
        return await db.submission.find_many(
            where={
                "formId": form_id
            },
            include={
                "user": True
            },
            order={
                "createdAt": "asc"
            }
        )