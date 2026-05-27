from app.features.forms.exceptions import (
    ArchivedProjectException,
    FormNotFoundException,
)
from app.features.forms.utils import (
    normalize_form_structure,
    structure_changed,
)


class GetFormUseCase:

    def __init__(self, form_repository, project_access_service):
        self.form_repository = form_repository
        self.project_access_service = project_access_service

    async def execute(self, form_id: str, user_id: str, user_email: str):
        form = await self.form_repository.find_by_id_with_project(form_id)

        if not form:
            raise FormNotFoundException()

        if form.project and form.project.deletedAt is not None:
            raise ArchivedProjectException()

        if not form.isPublic:
            await self.project_access_service.ensure_can_access_project(
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