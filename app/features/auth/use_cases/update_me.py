from app.infrastructure.security.password_service import hash_password


class UpdateMeUseCase:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, user_id: str, user_in):
        update_data = user_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = hash_password(
                update_data["password"]
            )

        return await self.user_repository.update(
            user_id,
            update_data
        )