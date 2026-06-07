from app.features.users.exceptions import (
    UserNotFoundException,
    UserUpdateException,
)
from app.infrastructure.security.password_service import hash_password


class UpdateUserUseCase:

    def __init__(self, repository):
        self.repository = repository

    async def execute(self, user_id: str, data: dict):
        user = await self.repository.find_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        try:
            if "password" in data and data["password"]:
                data["password"] = hash_password(data["password"])

            return await self.repository.update(
                user_id=user_id,
                data=data
            )

        except Exception as error:
            print(f"Erro ao atualizar usuário: {error}")
            raise UserUpdateException()