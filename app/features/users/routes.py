from fastapi import APIRouter, Depends, Query

from app.features.auth.dependencies import get_current_user

from app.features.users.schemas import (
    UserResponse,
    UserSimple,
    UserUpdate,
)

from app.features.users.dependencies import (
    get_search_users_use_case,
    get_user_use_case,
    get_update_user_use_case,
)

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse
)
async def get_me(
    current_user=Depends(get_current_user)
):
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse
)
async def update_me(
    data: UserUpdate,
    current_user=Depends(get_current_user),
    use_case=Depends(get_update_user_use_case)
):
    return await use_case.execute(
        user_id=current_user.id,
        data=data.model_dump(exclude_unset=True)
    )


@router.get(
    "/search",
    response_model=list[UserSimple]
)
async def search_users(
    q: str = Query(..., min_length=3),
    current_user=Depends(get_current_user),
    use_case=Depends(get_search_users_use_case)
):
    return await use_case.execute(
        query=q,
        current_user_id=current_user.id
    )


@router.get(
    "/{user_id}",
    response_model=UserSimple
)
async def get_user_by_id(
    user_id: str,
    current_user=Depends(get_current_user),
    use_case=Depends(get_user_use_case)
):
    return await use_case.execute(user_id)