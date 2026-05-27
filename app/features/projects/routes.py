from typing import List

from fastapi import APIRouter, Depends, status

from app.features.auth.dependencies import get_current_user

from app.features.projects.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectFullResponse,
)

from app.features.projects.dependencies import (
    get_create_project_use_case,
    get_list_projects_use_case,
    get_get_project_use_case,
    get_update_project_use_case,
    get_archive_project_use_case,
    get_restore_project_use_case,
    get_permanent_delete_project_use_case,
    get_list_archived_projects_use_case,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projetos"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectResponse
)
async def create_project(
    data: ProjectCreate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_create_project_use_case)
):
    return await use_case.execute(data, current_user.id)


@router.get(
    "/",
    response_model=List[ProjectResponse]
)
async def list_my_projects(
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_projects_use_case)
):
    return await use_case.execute(current_user.id)


@router.get(
    "/archived",
    response_model=List[ProjectResponse]
)
async def list_archived_projects(
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_archived_projects_use_case)
):
    return await use_case.execute(current_user.id)


@router.get(
    "/{project_id}",
    response_model=ProjectFullResponse
)
async def get_project(
    project_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_get_project_use_case)
):
    return await use_case.execute(
        project_id,
        current_user.id
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse
)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_update_project_use_case)
):
    return await use_case.execute(
        project_id,
        data,
        current_user.id
    )


@router.delete(
    "/{project_id}",
    response_model=ProjectResponse
)
async def archive_project(
    project_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_archive_project_use_case)
):
    return await use_case.execute(
        project_id,
        current_user.id
    )


@router.post(
    "/{project_id}/restore",
    response_model=ProjectResponse
)
async def restore_project(
    project_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_restore_project_use_case)
):
    return await use_case.execute(
        project_id,
        current_user.id
    )


@router.delete("/{project_id}/permanent")
async def permanent_delete_project(
    project_id: str,
    current_user = Depends(get_current_user),
    use_case = Depends(get_permanent_delete_project_use_case)
):
    return await use_case.execute(
        project_id,
        current_user.id
    )