from datetime import datetime

from app.infrastructure.security.password_service import hash_password
from app.features.auth.exceptions import (
    InvalidResetTokenException,
    ExpiredResetTokenException,
)


class ResetPasswordUseCase:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, token: str, new_password: str):
        user = await self.user_repository.find_by_reset_token(token)

        if not user:
            raise InvalidResetTokenException()

        expires_str = user.globalMetadata.get("reset_token_expires")

        if not expires_str:
            raise InvalidResetTokenException()

        if datetime.fromisoformat(expires_str) < datetime.now():
            raise ExpiredResetTokenException()

        metadata = user.globalMetadata or {}
        metadata.pop("reset_token", None)
        metadata.pop("reset_token_expires", None)

        await self.user_repository.update(
            user.id,
            {
                "password": hash_password(new_password),
                "globalMetadata": metadata,
            },
        )

        return {
            "message": "Senha alterada com sucesso!"
        }