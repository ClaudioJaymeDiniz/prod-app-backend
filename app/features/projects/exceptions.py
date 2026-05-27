from app.core.exceptions import BadRequestException, NotFoundException


class ProjectNotFoundException(NotFoundException):
    detail = "Projeto não encontrado"


class ProjectAccessDeniedException(NotFoundException):
    detail = "Projeto não encontrado"


class ProjectMustBeArchivedException(BadRequestException):
    detail = "O projeto precisa ser arquivado antes de ser excluído definitivamente"


class ProjectPermanentDeleteException(BadRequestException):
    detail = "Não foi possível excluir definitivamente o projeto"