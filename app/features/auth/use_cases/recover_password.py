import uuid
from datetime import datetime, timedelta


class RecoverPasswordUseCase:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, email: str):
        user = await self.user_repository.find_by_email(email)

        if not user:
            return {
                "message": "Se o e-mail existir, um link será enviado."
            }

        reset_token = str(uuid.uuid4())
        expires = datetime.now() + timedelta(hours=1)

        metadata = user.globalMetadata or {}
        metadata["reset_token"] = reset_token
        metadata["reset_token_expires"] = expires.isoformat()

        await self.user_repository.update(
            user.id,
            {
                "globalMetadata": metadata
            }
        )

        print(f"--- LINK DE RECUPERAÇÃO PARA {user.email} ---")
        print(f"http://localhost:3000/reset-password?token={reset_token}")
        print("---------------------------------------------")

        return {
            "message": "Link de recuperação enviado com sucesso."
        }