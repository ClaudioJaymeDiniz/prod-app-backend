import traceback

from app.features.projects.exceptions import (
    ProjectNotFoundException,
    ProjectMustBeArchivedException,
    ProjectPermanentDeleteException,
)


class PermanentDeleteProjectUseCase:

    def __init__(self, project_repository):
        self.project_repository = project_repository

    async def execute(self, project_id: str, user_id: str):
        project = await self.project_repository.find_by_id(project_id)

        if not project:
            return {
                "ok": True,
                "alreadyDeleted": True
            }

        if project.ownerId != user_id:
            raise ProjectNotFoundException()

        if project.deletedAt is None:
            raise ProjectMustBeArchivedException()

        try:
            await self.project_repository.delete_project_dependencies(
                project_id
            )

            deleted_project = await self.project_repository.delete_permanent(
                project_id
            )

            return deleted_project

        except Exception as error:
            print(f"Erro ao excluir projeto definitivamente ({project_id}): {error}")
            print(traceback.format_exc())

            raise ProjectPermanentDeleteException()