from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.features.auth.dependencies import get_current_user

from app.features.forms.schemas import (
    FormCreate,
    FormResponse,
    FormUpdate,
    FormPublicResponse,
    FormAnalyticsResponse,
)

from app.features.forms.dependencies import (
    get_create_form_use_case,
    get_list_project_forms_use_case,
    get_list_public_forms_use_case,
    get_get_form_use_case,
    get_update_form_use_case,
    get_archive_form_use_case,
    get_restore_form_use_case,
    get_permanent_delete_form_use_case,
    get_export_form_csv_use_case,
    get_form_analytics_use_case,
)


router = APIRouter(
    prefix="/forms",
    tags=["Formulários"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FormResponse
)
async def create_form(
    data: FormCreate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_create_form_use_case)
):
    return await use_case.execute(
        data,
        current_user.id
    )


@router.get(
    "/project/{project_id}",
    response_model=List[FormResponse]
)
async def list_project_forms(
    project_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_project_forms_use_case)
):
    return await use_case.execute(project_id)


@router.get(
    "/public",
    response_model=List[FormPublicResponse]
)
async def list_public_forms(
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_public_forms_use_case)
):
    return await use_case.execute()


@router.get(
    "/{form_id}",
    response_model=FormResponse
)
async def get_form_details(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_get_form_use_case)
):
    return await use_case.execute(
        form_id,
        current_user.id,
        current_user.email
    )


@router.patch(
    "/{form_id}",
    response_model=FormResponse
)
async def update_form(
    form_id: str,
    data: FormUpdate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_update_form_use_case)
):
    return await use_case.execute(
        form_id,
        data,
        current_user.id
    )


@router.get("/{form_id}/export/csv")
async def export_responses(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_export_form_csv_use_case)
):
    csv_data = await use_case.execute(
        form_id,
        current_user.id
    )

    filename = f"respostas_form_{form_id[:8]}.csv"

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers=headers
    )


@router.get(
    "/{form_id}/analytics",
    response_model=FormAnalyticsResponse
)
async def get_analytics(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_form_analytics_use_case)
):
    return await use_case.execute(
        form_id,
        current_user.id
    )


@router.delete(
    "/{form_id}",
    response_model=FormResponse
)
async def archive_form(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_archive_form_use_case)
):
    return await use_case.execute(
        form_id,
        current_user.id
    )


@router.post(
    "/{form_id}/restore",
    response_model=FormResponse
)
async def restore_form(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_restore_form_use_case)
):
    return await use_case.execute(
        form_id,
        current_user.id
    )


@router.delete("/{form_id}/permanent")
async def permanent_delete_form(
    form_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_permanent_delete_form_use_case)
):
    return await use_case.execute(
        form_id,
        current_user.id
    )