from app.features.projects.exceptions import (
    ProjectNotFoundException
)


class ListProjectMembersUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(
        self,
        project_id: str,
        owner_id: str
    ):
        project = await self.invitation_repository.find_project_by_id(
            project_id
        )

        if not project or project.ownerId != owner_id:
            raise ProjectNotFoundException()

        return await self.invitation_repository.list_project_members(
            project_id
        )