from app.features.forms.exceptions import (
    ArchivedProjectException,
    FormNotFoundException,
)
from app.features.forms.utils import (
    normalize_form_structure,
    structure_changed,
)


class GetFormUseCase:

    def __init__(self, form_repository, invitation_repository):
        self.form_repository = form_repository
        self.invitation_repository = invitation_repository

    async def execute(self, form_id: str, user_id: str, user_email: str):
        form = await self.form_repository.find_by_id_with_project(form_id)

        if not form:
            raise FormNotFoundException()

        if form.project and form.project.deletedAt is not None:
            raise ArchivedProjectException()

        if not form.isPublic:
            await self._check_access(
                form.projectId,
                user_id,
                user_email
            )

        normalized_structure = normalize_form_structure(
            form.structure or []
        )

        if structure_changed(form.structure or [], normalized_structure):
            form = await self.form_repository.update(
                form.id,
                {
                    "structure": normalized_structure
                }
            )

        return form

    async def _check_access(
        self,
        project_id: str,
        user_id: str,
        email: str
    ):
        project = await self.invitation_repository.find_project_by_id(
            project_id
        )

        if not project:
            raise FormNotFoundException()

        # OWNER
        if project.ownerId == user_id:
            return

        # convite aceito
        accepted_invitation = (
            await self.invitation_repository
            .find_accepted_by_project_and_email(
                project_id,
                email
            )
        )

        if accepted_invitation:
            return

        raise FormNotFoundException()