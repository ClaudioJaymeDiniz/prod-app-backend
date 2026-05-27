from app.infrastructure.database.prisma_client import db
from app.features.users.repositories import UserRepository


class PrismaUserRepository(UserRepository):

    async def create(self, data: dict):
        return await db.user.create(data=data)

    async def find_by_email(self, email: str):
        return await db.user.find_unique(
            where={"email": email}
        )

    async def find_by_id(self, user_id: str):
        return await db.user.find_unique(
            where={"id": user_id}
        )

    async def update(self, user_id: str, data: dict):
        return await db.user.update(
            where={"id": user_id},
            data=data
        )

    async def find_by_reset_token(self, token: str):
        return await db.user.find_first(
            where={
                "globalMetadata": {
                    "path": ["reset_token"],
                    "equals": token
                }
            }
        )