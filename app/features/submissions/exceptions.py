from app.core.exceptions import BadRequestException, NotFoundException


class InvalidSubmissionPayloadException(BadRequestException):
    detail = "Payload inválido. Campos obrigatórios: id, formId e formData."


class InvalidSubmissionDataException(BadRequestException):
    detail = "Os dados enviados não respeitam a estrutura do formulário."

    def __init__(self, errors: list):
        self.detail = {
            "message": "Os dados enviados não respeitam a estrutura do formulário.",
            "errors": errors
        }


class SubmissionAlreadyExistsException(BadRequestException):
    detail = "Submissão já registrada."


class SubmissionNotFoundException(NotFoundException):
    detail = "Resposta não encontrada."


class SubmissionAccessDeniedException(NotFoundException):
    detail = "Resposta não encontrada."


class FormNotAvailableForSubmissionException(BadRequestException):
    detail = "Projeto arquivado não pode receber respostas."


class SubmissionUpdatePayloadException(BadRequestException):
    detail = "formData é obrigatório para atualização."


class SubmissionCreateException(BadRequestException):
    detail = "Erro interno ao processar a coleta de dados."