from fastapi import Depends

from app.features.forms.prisma_repository import PrismaFormRepository
from app.features.invitations.prisma_repository import PrismaInvitationRepository

from app.features.forms.use_cases.create_form import CreateFormUseCase
from app.features.forms.use_cases.list_project_forms import ListProjectFormsUseCase
from app.features.forms.use_cases.list_public_forms import ListPublicFormsUseCase
from app.features.forms.use_cases.get_form import GetFormUseCase
from app.features.forms.use_cases.update_form import UpdateFormUseCase
from app.features.forms.use_cases.archive_form import ArchiveFormUseCase
from app.features.forms.use_cases.restore_form import RestoreFormUseCase
from app.features.forms.use_cases.permanent_delete_form import PermanentDeleteFormUseCase
from app.features.forms.use_cases.export_form_csv import ExportFormCsvUseCase
from app.features.forms.use_cases.get_form_analytics import GetFormAnalyticsUseCase


def get_form_repository():
    return PrismaFormRepository()


def get_invitation_repository():
    return PrismaInvitationRepository()


def get_create_form_use_case(
    form_repository = Depends(get_form_repository)
):
    return CreateFormUseCase(form_repository)


def get_list_project_forms_use_case(
    form_repository = Depends(get_form_repository)
):
    return ListProjectFormsUseCase(form_repository)


def get_list_public_forms_use_case(
    form_repository = Depends(get_form_repository)
):
    return ListPublicFormsUseCase(form_repository)


def get_get_form_use_case(
    form_repository = Depends(get_form_repository),
    invitation_repository = Depends(get_invitation_repository)
):
    return GetFormUseCase(
        form_repository,
        invitation_repository
    )


def get_update_form_use_case(
    form_repository = Depends(get_form_repository)
):
    return UpdateFormUseCase(form_repository)


def get_archive_form_use_case(
    form_repository = Depends(get_form_repository)
):
    return ArchiveFormUseCase(form_repository)


def get_restore_form_use_case(
    form_repository = Depends(get_form_repository)
):
    return RestoreFormUseCase(form_repository)


def get_permanent_delete_form_use_case(
    form_repository = Depends(get_form_repository)
):
    return PermanentDeleteFormUseCase(form_repository)


def get_export_form_csv_use_case(
    form_repository = Depends(get_form_repository)
):
    return ExportFormCsvUseCase(form_repository)


def get_form_analytics_use_case(
    form_repository = Depends(get_form_repository)
):
    return GetFormAnalyticsUseCase(form_repository)