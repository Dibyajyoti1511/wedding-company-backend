from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd.verify(plain, hashed)
