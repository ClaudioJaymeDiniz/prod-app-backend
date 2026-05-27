class ListPublicFormsUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self):
        forms = await self.form_repository.list_public()

        active_project_forms = [
            form
            for form in forms
            if form.project and form.project.deletedAt is None
        ]

        return [
            {
                "id": form.id,
                "title": form.title,
                "description": form.description,
                "isPublic": form.isPublic,
                "projectId": form.projectId,
                "projectName": form.project.name,
                "projectColor": form.project.themeColor,
                "ownerId": form.project.ownerId,
            }
            for form in active_project_forms
        ]