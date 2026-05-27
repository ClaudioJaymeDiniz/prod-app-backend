from fastapi import Depends
from app.features.invitations.prisma_repository import PrismaInvitationRepository
from app.features.projects.services.project_access_service import ProjectAccessService

from app.features.projects.prisma_repository import PrismaProjectRepository

from app.features.projects.use_cases.create_project import CreateProjectUseCase
from app.features.projects.use_cases.list_projects import ListProjectsUseCase
from app.features.projects.use_cases.get_project import GetProjectUseCase
from app.features.projects.use_cases.update_project import UpdateProjectUseCase
from app.features.projects.use_cases.archive_project import ArchiveProjectUseCase
from app.features.projects.use_cases.restore_project import RestoreProjectUseCase
from app.features.projects.use_cases.permanent_delete_project import PermanentDeleteProjectUseCase
from app.features.projects.use_cases.list_archived_projects import ListArchivedProjectsUseCase


def get_project_repository():
    return PrismaProjectRepository()


def get_create_project_use_case(
    project_repository = Depends(get_project_repository)
):
    return CreateProjectUseCase(project_repository)


def get_list_projects_use_case(
    project_repository = Depends(get_project_repository)
):
    return ListProjectsUseCase(project_repository)


def get_get_project_use_case(
    project_repository = Depends(get_project_repository)
):
    return GetProjectUseCase(project_repository)


def get_update_project_use_case(
    project_repository = Depends(get_project_repository)
):
    return UpdateProjectUseCase(project_repository)


def get_archive_project_use_case(
    project_repository = Depends(get_project_repository)
):
    return ArchiveProjectUseCase(project_repository)


def get_restore_project_use_case(
    project_repository = Depends(get_project_repository)
):
    return RestoreProjectUseCase(project_repository)


def get_permanent_delete_project_use_case(
    project_repository = Depends(get_project_repository)
):
    return PermanentDeleteProjectUseCase(project_repository)


def get_list_archived_projects_use_case(
    project_repository = Depends(get_project_repository)
):
    return ListArchivedProjectsUseCase(project_repository)

def get_invitation_repository():
    return PrismaInvitationRepository()


def get_project_access_service(
    project_repository = Depends(get_project_repository),
    invitation_repository = Depends(get_invitation_repository)
):
    return ProjectAccessService(
        project_repository,
        invitation_repository
    )