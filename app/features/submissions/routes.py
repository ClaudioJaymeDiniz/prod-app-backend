from typing import List

from fastapi import APIRouter, Depends, status

from app.features.auth.dependencies import get_current_user

from app.features.submissions.schemas import (
    SubmissionCreate,
    SubmissionResponse,
    SubmissionUpdate,
)

from app.features.submissions.dependencies import (
    get_create_submission_use_case,
    get_update_submission_use_case,
    get_list_my_submissions_use_case,
    get_list_form_submissions_use_case,
    get_list_all_form_submissions_use_case,
)


router = APIRouter(
    prefix="/submissions",
    tags=["Submissões"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SubmissionResponse
)
async def submit_form(
    data: SubmissionCreate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_create_submission_use_case)
):
    submission_data = data.model_dump()

    return await use_case.execute(
        submission_data,
        current_user.id,
        current_user.email
    )


@router.patch(
    "/{submission_id}",
    response_model=SubmissionResponse
)
async def update_my_submission(
    submission_id: str,
    data: SubmissionUpdate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_update_submission_use_case)
):
    return await use_case.execute(
        submission_id,
        data,
        current_user.id
    )


@router.get(
    "/me",
    response_model=List[SubmissionResponse]
)
async def list_my_responses(
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_my_submissions_use_case)
):
    return await use_case.execute(
        current_user.id
    )


@router.get(
    "/form/{form_id}",
    response_model=List[SubmissionResponse]
)
async def list_form_submissions(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_form_submissions_use_case)
):
    return await use_case.execute(
        form_id,
        current_user.id
    )


@router.get(
    "/form/{form_id}/all",
    response_model=List[SubmissionResponse]
)
async def list_all_form_submissions(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_all_form_submissions_use_case)
):
    return await use_case.execute(
        form_id,
        current_user.id
    )