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

    async def find_invitation_by_id(self, invitation_id: str):
        return await db.projectinvitation.find_unique(
            where={
                "id": invitation_id
            },
            include={
                "project": {
                    "include": {
                        "owner": True,
                        "members": {
                            "include": {
                                "user": True
                            }
                        }
                    }
                }
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

    async def update_invitation_status(
        self,
        invitation_id: str,
        status: str,
        user_id: str | None = None,
    ):
        data = {"status": status}
        if user_id is not None:
            data["userId"] = user_id

        return await db.projectinvitation.update(
            where={
                "id": invitation_id
            },
            data=data,
            include={
                "project": {
                    "include": {
                        "owner": True
                    }
                }
            }
        )
    
    async def list_pending_by_project(self, project_id: str):
        return await db.projectinvitation.find_many(
            where={
                "projectId": project_id,
                "status": "PENDING"
            },
            include={
                "project": {
                    "include": {
                        "owner": True
                    }
                }
            }
        )