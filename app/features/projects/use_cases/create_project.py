class CreateProjectUseCase:

    def __init__(self, project_repository):
        self.project_repository = project_repository

    async def execute(self, data, user_id: str):
        return await self.project_repository.create(
            {
                "name": data.name,
                "description": data.description,
                "isPublic": data.isPublic,
                "logoUrl": data.logoUrl,
                "themeColor": data.themeColor,
                "ownerId": user_id,
                "members": {
                    "create": {
                        "userId": user_id,
                        "role": "OWNER"
                    }
                }
            }
        )