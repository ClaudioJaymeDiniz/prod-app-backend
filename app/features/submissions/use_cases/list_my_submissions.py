class ListMySubmissionsUseCase:

    def __init__(self, submission_repository):
        self.submission_repository = submission_repository

    async def execute(self, user_id: str):
        return await self.submission_repository.list_by_user(user_id)