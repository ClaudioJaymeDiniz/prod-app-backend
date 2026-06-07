from app.features.users.exceptions import InvalidUserSearchException


class SearchUsersUseCase:

    def __init__(self, repository):
        self.repository = repository

    async def execute(
        self,
        query: str,
        current_user_id: str
    ):
        query = query.strip()

        if len(query) < 3:
            raise InvalidUserSearchException()

        users = await self.repository.search(query)

        return [
            user
            for user in users
            if user.id != current_user_id
        ]