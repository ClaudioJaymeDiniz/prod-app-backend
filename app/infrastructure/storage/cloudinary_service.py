import cloudinary
import cloudinary.uploader

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


class CloudinaryService:

    async def upload_image(
        self,
        file,
        folder: str,
        user_id: str
    ) -> str:
        result = cloudinary.uploader.upload(
    file,
    folder=f"smart_forms/{folder}",
    resource_type="image",
    tags=[
        f"user_{user_id}",
        "tcc_project"
    ],
    quality="auto:good",
    fetch_format="auto",
    transformation=[
        {
            "width": 1600,
            "height": 1600,
            "crop": "limit"
        }
    ]
)
        return result.get("secure_url")