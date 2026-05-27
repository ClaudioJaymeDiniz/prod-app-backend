from app.features.auth.exceptions import InvalidCredentialsException
from app.infrastructure.security.password_service import verify_password


class LoginUseCase:

    def __init__(self, user_repository, jwt_service):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(self, email: str, password: str):
        user = await self.user_repository.find_by_email(email)

        if not user or not verify_password(password, user.password):
           raise InvalidCredentialsException()

        token = self.jwt_service.create_access_token(
            {
                "sub": user.id,
                "email": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }