class GetMeUseCase:

    async def execute(self, current_user):
        return current_user