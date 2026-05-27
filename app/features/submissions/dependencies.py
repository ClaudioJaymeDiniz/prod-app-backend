from fastapi import Depends

from app.features.submissions.prisma_repository import PrismaSubmissionRepository

from app.features.projects.dependencies import get_project_access_service

from app.features.submissions.use_cases.create_submission import CreateSubmissionUseCase
from app.features.submissions.use_cases.update_submission import UpdateSubmissionUseCase
from app.features.submissions.use_cases.list_my_submissions import ListMySubmissionsUseCase
from app.features.submissions.use_cases.list_form_submissions import ListFormSubmissionsUseCase
from app.features.submissions.use_cases.list_all_form_submissions import ListAllFormSubmissionsUseCase


def get_submission_repository():
    return PrismaSubmissionRepository()

def get_create_submission_use_case(
    submission_repository = Depends(get_submission_repository),
    project_access_service = Depends(get_project_access_service)
):
    return CreateSubmissionUseCase(
        submission_repository,
        project_access_service
    )

def get_update_submission_use_case(
    submission_repository = Depends(get_submission_repository)
):
    return UpdateSubmissionUseCase(submission_repository)


def get_list_my_submissions_use_case(
    submission_repository = Depends(get_submission_repository)
):
    return ListMySubmissionsUseCase(submission_repository)


def get_list_form_submissions_use_case(
    submission_repository = Depends(get_submission_repository)
):
    return ListFormSubmissionsUseCase(submission_repository)


def get_list_all_form_submissions_use_case(
    submission_repository = Depends(get_submission_repository)
):
    return ListAllFormSubmissionsUseCase(submission_repository)