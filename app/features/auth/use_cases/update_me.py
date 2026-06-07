from app.infrastructure.security.password_service import hash_password


class UpdateMeUseCase:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, user_id: str, user_in):
        update_data = user_in.model_dump(exclude_unset=True)

        if "globalMetadata" in update_data and update_data["globalMetadata"] is not None:
            current_user = await self.user_repository.find_by_id(user_id)
            current_metadata = current_user.globalMetadata or {}
            incoming_metadata = update_data["globalMetadata"] or {}

            if not isinstance(current_metadata, dict):
                current_metadata = {}

            if not isinstance(incoming_metadata, dict):
                incoming_metadata = {}

            merged_metadata = {**current_metadata, **incoming_metadata}
            update_data["globalMetadata"] = merged_metadata

        if "password" in update_data:
            update_data["password"] = hash_password(
                update_data["password"]
            )

        return await self.user_repository.update(
            user_id,
            update_data
        )