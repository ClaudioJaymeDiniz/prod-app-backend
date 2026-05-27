from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.features.users.prisma_repository import PrismaUserRepository
from app.infrastructure.auth.jwt_service import JWTService

from app.features.auth.use_cases.register import RegisterUseCase
from app.features.auth.use_cases.login import LoginUseCase
from app.features.auth.use_cases.get_me import GetMeUseCase
from app.features.auth.use_cases.update_me import UpdateMeUseCase
from app.features.auth.use_cases.recover_password import RecoverPasswordUseCase
from app.features.auth.use_cases.reset_password import ResetPasswordUseCase


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_user_repository():
    return PrismaUserRepository()


def get_jwt_service():
    return JWTService()


def get_register_use_case(
    user_repository = Depends(get_user_repository)
):
    return RegisterUseCase(user_repository)


def get_login_use_case(
    user_repository = Depends(get_user_repository),
    jwt_service = Depends(get_jwt_service)
):
    return LoginUseCase(user_repository, jwt_service)


def get_get_me_use_case():
    return GetMeUseCase()


def get_update_me_use_case(
    user_repository = Depends(get_user_repository)
):
    return UpdateMeUseCase(user_repository)


def get_recover_password_use_case(
    user_repository = Depends(get_user_repository)
):
    return RecoverPasswordUseCase(user_repository)


def get_reset_password_use_case(
    user_repository = Depends(get_user_repository)
):
    return ResetPasswordUseCase(user_repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository = Depends(get_user_repository),
    jwt_service = Depends(get_jwt_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt_service.decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = await user_repository.find_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user