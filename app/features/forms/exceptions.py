from app.core.exceptions import BadRequestException, NotFoundException


class FormNotFoundException(NotFoundException):
    detail = "Formulário não encontrado"


class FormProjectAccessDeniedException(NotFoundException):
    detail = "Projeto não encontrado"


class FormAccessDeniedException(NotFoundException):
    detail = "Formulário não encontrado"


class ArchivedProjectException(BadRequestException):
    detail = "Projeto arquivado"


class FormMustBeArchivedException(BadRequestException):
    detail = "O formulário precisa ser arquivado antes de ser excluído definitivamente"


class FormCsvExportException(BadRequestException):
    detail = "Não foi possível exportar as respostas do formulário"