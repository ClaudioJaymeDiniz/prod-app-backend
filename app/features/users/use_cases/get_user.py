from app.features.users.exceptions import UserNotFoundException


class GetUserUseCase:

    def __init__(self, repository):
        self.repository = repository

    async def execute(self, user_id: str):
        user = await self.repository.find_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        return user