from app.repositories.master_repo import MasterRepo
from app.utils.hashing import Hasher
from app.utils.jwt_handler import JWTHandler

class AuthService:
    def __init__(self):
        self.repo = MasterRepo()

    def admin_login(self, email: str, password: str):
        admin = self.repo.find_admin_by_email(email)
        if not admin:
            return None
        if not Hasher.verify_password(password, admin["password"]):
            return None
        token = JWTHandler.create_token(str(admin["_id"]), admin["organization"])
        return token
