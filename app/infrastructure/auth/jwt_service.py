from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings


class JWTService:

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            raise ValueError("Token inválido ou expirado")