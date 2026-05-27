from app.core.exceptions import BadRequestException, UnauthorizedException


class UserAlreadyExistsException(BadRequestException):
    detail = "Usuário já cadastrado."


class InvalidCredentialsException(UnauthorizedException):
    detail = "E-mail ou senha incorretos."


class InvalidTokenException(UnauthorizedException):
    detail = "Token inválido ou expirado"


class InvalidResetTokenException(BadRequestException):
    detail = "Token inválido ou expirado."


class ExpiredResetTokenException(BadRequestException):
    detail = "Token expirado."