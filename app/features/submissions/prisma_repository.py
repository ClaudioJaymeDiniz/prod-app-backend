from prisma import Json

from app.infrastructure.database.prisma_client import db
from app.features.submissions.repositories import SubmissionRepository


class PrismaSubmissionRepository(SubmissionRepository):

    async def create(self, data: dict):
        if "formData" in data:
            data["formData"] = Json(data["formData"])

        return await db.submission.create(data=data)

    async def update(self, submission_id: str, data: dict):
        if "formData" in data:
            data["formData"] = Json(data["formData"])

        return await db.submission.update(
            where={"id": submission_id},
            data=data
        )

    async def find_by_id(self, submission_id: str):
        return await db.submission.find_unique(
            where={"id": submission_id}
        )

    async def find_form_by_id(self, form_id: str):
        return await db.form.find_unique(
            where={"id": form_id},
            include={"project": True}
        )

    async def find_form_with_project_owner(self, form_id: str):
        return await db.form.find_unique(
            where={"id": form_id},
            include={
                "project": {
                    "include": {
                        "owner": True
                    }
                }
            }
        )

    async def list_by_user(self, user_id: str):
        return await db.submission.find_many(
            where={"userId": user_id},
            order={"createdAt": "desc"}
        )

    async def list_by_form(self, form_id: str):
        return await db.submission.find_many(
            where={"formId": form_id},
            include={"user": True},
            order={"createdAt": "desc"}
        )

    async def list_by_form_and_user(self, form_id: str, user_id: str):
        return await db.submission.find_many(
            where={
                "formId": form_id,
                "userId": user_id
            },
            order={"createdAt": "desc"}
        )