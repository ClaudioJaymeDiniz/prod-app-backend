from fastapi import APIRouter, Depends, File, UploadFile

from app.features.auth.dependencies import get_current_user
from app.features.uploads.schemas import UploadImageResponse
from app.features.uploads.dependencies import get_upload_image_use_case


router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


@router.post(
    "/image",
    response_model=UploadImageResponse
)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = "submissions",
    current_user = Depends(get_current_user),
    use_case = Depends(get_upload_image_use_case)
):
    return await use_case.execute(
        file=file.file,
        filename=file.filename,
        folder=folder,
        user_id=current_user.id
    )