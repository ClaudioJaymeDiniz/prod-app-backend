from app.core.exceptions import BadRequestException, NotFoundException


class InvitationProjectAccessDeniedException(NotFoundException):
    detail = "Projeto não encontrado"


class InvitationAlreadyExistsException(BadRequestException):
    detail = "Convite já existe para este e-mail neste projeto"


class InvitationCreateException(BadRequestException):
    detail = "Não foi possível criar o convite"