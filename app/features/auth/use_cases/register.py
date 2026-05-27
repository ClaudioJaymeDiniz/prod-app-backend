from app.features.users.schemas import UserCreate
from app.infrastructure.security.password_service import hash_password
from app.features.auth.exceptions import UserAlreadyExistsException

class RegisterUseCase:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, user_in: UserCreate):
        user_exists = await self.user_repository.find_by_email(
            user_in.email
        )

        if user_exists:
            raise UserAlreadyExistsException()

        return await self.user_repository.create(
            {
                "email": user_in.email,
                "name": user_in.name,
                "password": hash_password(user_in.password),
                "provider": "local"
            }
        )
    
    