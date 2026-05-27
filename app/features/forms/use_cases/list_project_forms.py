from app.features.forms.utils import (
    normalize_form_structure,
    structure_changed,
)


class ListProjectFormsUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self, project_id: str):
        forms = await self.form_repository.list_by_project(project_id)

        response = []

        for form in forms:
            normalized_structure = normalize_form_structure(
                form.structure or []
            )

            if structure_changed(form.structure or [], normalized_structure):
                await self.form_repository.update(
                    form.id,
                    {
                        "structure": normalized_structure
                    }
                )

            response.append(
                {
                    "id": form.id,
                    "title": form.title,
                    "description": form.description,
                    "isPublic": form.isPublic,
                    "structure": normalized_structure,
                    "projectId": form.projectId,
                    "createdAt": form.createdAt,
                    "deletedAt": form.deletedAt,
                    "submissionCount": len(form.submissions),
                }
            )

        return response