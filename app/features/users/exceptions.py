from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
)


class UserNotFoundException(NotFoundException):
    detail = "Usuário não encontrado."


class InvalidUserSearchException(BadRequestException):
    detail = "Informe pelo menos 3 caracteres para buscar usuários."


class UserUpdateException(BadRequestException):
    detail = "Erro ao atualizar usuário."