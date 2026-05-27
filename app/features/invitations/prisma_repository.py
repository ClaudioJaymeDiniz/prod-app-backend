from app.infrastructure.database.prisma_client import db
from app.features.invitations.repositories import InvitationRepository


class PrismaInvitationRepository(InvitationRepository):

    async def create(self, data: dict):
        return await db.projectinvitation.create(
            data=data
        )

    async def find_project_by_id(self, project_id: str):
        return await db.project.find_unique(
            where={
                "id": project_id
            }
        )

    async def find_user_by_email(self, email: str):
        return await db.user.find_unique(
            where={
                "email": email
            }
        )

    async def upsert_project_member(
        self,
        user_id: str,
        project_id: str,
        role: str
    ):
        return await db.userproject.upsert(
            where={
                "userId_projectId": {
                    "userId": user_id,
                    "projectId": project_id
                }
            },
            data={
                "update": {
                    "role": role
                },
                "create": {
                    "userId": user_id,
                    "projectId": project_id,
                    "role": role
                }
            }
        )

    async def list_pending_by_email(self, email: str):
        return await db.projectinvitation.find_many(
            where={
                "email": {
                    "equals": email,
                    "mode": "insensitive"
                },
                "status": "PENDING"
            },
            include={
                "project": {
                    "include": {
                        "owner": True
                    }
                }
            },
            order={
                "createdAt": "desc"
            }
        )
    
    async def find_accepted_by_project_and_email(
        self,
        project_id: str,
        email: str
    ):
        return await db.projectinvitation.find_first(
            where={
                "projectId": project_id,
                "email": {
                    "equals": email,
                    "mode": "insensitive"
                },
                "status": "ACCEPTED"
            }
        )