from app.infrastructure.database.prisma_client import db
from app.features.projects.repositories import ProjectRepository


class PrismaProjectRepository(ProjectRepository):

    async def create(self, data: dict):
        return await db.project.create(data=data)

    async def find_by_id(self, project_id: str):
        return await db.project.find_unique(
            where={"id": project_id}
        )

    async def find_full_by_id(self, project_id: str):
        return await db.project.find_unique(
            where={"id": project_id},
            include={
                "owner": True,
                "members": {
                    "include": {
                        "user": True
                    }
                }
            }
        )

    async def list_by_user(self, user_id: str):
        return await db.project.find_many(
            where={
                "deletedAt": None,
                "OR": [
                    {"ownerId": user_id},
                    {
                        "members": {
                            "some": {
                                "userId": user_id
                            }
                        }
                    }
                ]
            },
            include={
                "owner": True,
                "forms": True
            },
            order={
                "createdAt": "desc"
            }
        )

    async def list_archived_by_owner(self, owner_id: str):
        return await db.project.find_many(
            where={
                "ownerId": owner_id,
                "NOT": {
                    "deletedAt": None
                }
            },
            order={
                "deletedAt": "desc"
            }
        )

    async def update(self, project_id: str, data: dict):
        return await db.project.update(
            where={"id": project_id},
            data=data
        )

    async def delete_project_dependencies(self, project_id: str):
        forms = await db.form.find_many(
            where={"projectId": project_id}
        )

        for form in forms:
            await db.submission.delete_many(
                where={"formId": form.id}
            )

        await db.form.delete_many(
            where={"projectId": project_id}
        )

        await db.projectinvitation.delete_many(
            where={"projectId": project_id}
        )

        await db.userproject.delete_many(
            where={"projectId": project_id}
        )

    async def delete_permanent(self, project_id: str):
        return await db.project.delete(
            where={"id": project_id}
        )