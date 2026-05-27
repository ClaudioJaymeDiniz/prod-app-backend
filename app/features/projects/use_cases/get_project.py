from app.features.projects.exceptions import ProjectNotFoundException


class GetProjectUseCase:

    def __init__(self, project_repository):
        self.project_repository = project_repository

    async def execute(self, project_id: str, user_id: str):
        project = await self.project_repository.find_full_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        is_owner = project.ownerId == user_id

        is_member = any(
            member.userId == user_id
            for member in project.members
        )

        if not is_owner and not is_member:
            raise ProjectNotFoundException()

        return project