from app.features.uploads.exceptions import (
    InvalidImageFormatException,
    UploadImageException,
    ImageTooLargeException,
)


class UploadImageUseCase:

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    def __init__(self, storage_service):
        self.storage_service = storage_service

    async def execute(
        self,
        file,
        filename: str,
        folder: str,
        user_id: str
    ):
        allowed_extensions = [
            "jpg",
            "jpeg",
            "png",
            "webp"
        ]

        file_ext = filename.split(".")[-1].lower()

        if file_ext not in allowed_extensions:
            raise InvalidImageFormatException()

        content = file.read()

        if len(content) > self.MAX_FILE_SIZE:
            raise ImageTooLargeException()

        try:
            url = await self.storage_service.upload_image(
                file=content,
                folder=folder,
                user_id=user_id
            )

            return {
                "url": url
            }

        except Exception as error:
            print(f"Erro no upload: {error}")
            raise UploadImageException()