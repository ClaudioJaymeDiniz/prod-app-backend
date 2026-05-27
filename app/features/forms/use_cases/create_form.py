from prisma import Json

from app.features.forms.exceptions import FormProjectAccessDeniedException
from app.features.forms.utils import normalize_form_structure


class CreateFormUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self, data, user_id: str):
        project = await self.form_repository.find_project_by_id(
            data.projectId
        )

        if not project or project.ownerId != user_id:
            raise FormProjectAccessDeniedException()

        fields_json = normalize_form_structure(
            [
                field.model_dump()
                for field in data.structure
            ]
        )

        return await self.form_repository.create(
            {
                "title": data.title,
                "description": data.description,
                "isPublic": data.isPublic,
                "structure": Json(fields_json),
                "projectId": data.projectId
            }
        )