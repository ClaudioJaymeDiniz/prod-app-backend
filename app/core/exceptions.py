class AppException(Exception):
    status_code = 500
    detail = "Erro interno"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class BadRequestException(AppException):
    status_code = 400
    detail = "Requisição inválida"


class UnauthorizedException(AppException):
    status_code = 401
    detail = "Não autorizado"


class NotFoundException(AppException):
    status_code = 404
    detail = "Recurso não encontrado"