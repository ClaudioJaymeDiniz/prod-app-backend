from app.core.exceptions import BadRequestException


class InvalidImageFormatException(BadRequestException):
    detail = "Formato de imagem inválido."


class ImageTooLargeException(BadRequestException):
    detail = "Imagem muito grande. Máximo permitido: 5MB."


class UploadImageException(BadRequestException):
    detail = "Erro ao realizar upload da imagem."