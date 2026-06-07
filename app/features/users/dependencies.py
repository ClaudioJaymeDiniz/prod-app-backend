from app.features.users.prisma_repository import PrismaUserRepository

from app.features.users.use_cases.search_users import SearchUsersUseCase
from app.features.users.use_cases.get_user import GetUserUseCase
from app.features.users.use_cases.update_user import UpdateUserUseCase


def get_user_repository():
    return PrismaUserRepository()


def get_search_users_use_case():
    return SearchUsersUseCase(
        repository=get_user_repository()
    )


def get_user_use_case():
    return GetUserUseCase(
        repository=get_user_repository()
    )


def get_update_user_use_case():
    return UpdateUserUseCase(
        repository=get_user_repository()
    )