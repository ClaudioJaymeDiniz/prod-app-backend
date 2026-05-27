from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.features.users.schemas import UserCreate, UserUpdate, UserResponse
from app.features.auth.schemas import (
    TokenResponse,
    PasswordRecoveryRequest,
    PasswordReset,
)

from app.features.auth.dependencies import (
    get_current_user,
    get_register_use_case,
    get_login_use_case,
    get_get_me_use_case,
    get_update_me_use_case,
    get_recover_password_use_case,
    get_reset_password_use_case,
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    use_case = Depends(get_register_use_case)
):
    return await use_case.execute(user_in)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    use_case = Depends(get_login_use_case)
):
    return await use_case.execute(
        credentials.username,
        credentials.password
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user = Depends(get_current_user),
    use_case = Depends(get_get_me_use_case)
):
    return await use_case.execute(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    user_in: UserUpdate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_update_me_use_case)
):
    return await use_case.execute(
        current_user.id,
        user_in
    )


@router.post("/recover-password")
async def recover_password(
    data: PasswordRecoveryRequest,
    use_case = Depends(get_recover_password_use_case)
):
    return await use_case.execute(data.email)


@router.post("/reset-password")
async def reset_password(
    data: PasswordReset,
    use_case = Depends(get_reset_password_use_case)
):
    return await use_case.execute(
        data.token,
        data.new_password
    )