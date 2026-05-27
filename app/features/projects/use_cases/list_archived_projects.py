class ListArchivedProjectsUseCase:

    def __init__(self, project_repository):
        self.project_repository = project_repository

    async def execute(self, user_id: str):
        return await self.project_repository.list_archived_by_owner(user_id)