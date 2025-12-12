import jwt
from datetime import datetime, timedelta
from app.config import settings

class JWTHandler:
    @staticmethod
    def create_token(admin_id: str, organization: str):
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXP_HOURS)
        payload = {
            "admin_id": str(admin_id),
            "organization": organization,
            "exp": expire,
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_token(token: str):
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
