from fastapi import Depends

from app.infrastructure.storage.cloudinary_service import CloudinaryService
from app.features.uploads.use_cases.upload_image import UploadImageUseCase


def get_storage_service():
    return CloudinaryService()


def get_upload_image_use_case(
    storage_service = Depends(get_storage_service)
):
    return UploadImageUseCase(storage_service)