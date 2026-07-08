import bcrypt
import jwt

from core.settings import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def create_access_token(data: dict[str, str]):
    encoded_jwt = jwt.encode(
        data, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
