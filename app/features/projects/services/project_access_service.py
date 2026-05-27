from app.features.projects.exceptions import ProjectNotFoundException


class ProjectAccessService:

    def __init__(self, project_repository, invitation_repository):
        self.project_repository = project_repository
        self.invitation_repository = invitation_repository

    async def ensure_owner(self, project_id: str, user_id: str):
        project = await self.project_repository.find_by_id(project_id)

        if not project or project.ownerId != user_id:
            raise ProjectNotFoundException()

        return project

    async def ensure_can_access_project(
        self,
        project_id: str,
        user_id: str,
        user_email: str
    ):
        project = await self.project_repository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        if project.ownerId == user_id:
            return project

        accepted_invitation = (
            await self.invitation_repository
            .find_accepted_by_project_and_email(
                project_id,
                user_email
            )
        )

        if accepted_invitation:
            return project

        raise ProjectNotFoundException()

    async def ensure_can_submit_to_project(
        self,
        project_id: str,
        user_id: str,
        user_email: str
    ):
        return await self.ensure_can_access_project(
            project_id,
            user_id,
            user_email
        )