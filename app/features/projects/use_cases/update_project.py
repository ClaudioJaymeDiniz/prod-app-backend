from app.features.projects.exceptions import ProjectNotFoundException


class UpdateProjectUseCase:

    def __init__(self, project_repository):
        self.project_repository = project_repository

    async def execute(self, project_id: str, data, user_id: str):
        project = await self.project_repository.find_by_id(project_id)

        if not project or project.ownerId != user_id:
            raise ProjectNotFoundException()

        update_data = data.model_dump(exclude_unset=True)

        return await self.project_repository.update(
            project_id,
            update_data
        )