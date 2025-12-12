from fastapi import APIRouter, HTTPException
from app.models.schemas import AdminLoginSchema, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin", tags=["admin"])
auth_svc = AuthService()

@router.post("/login", response_model=TokenResponse)
def login(payload: AdminLoginSchema):
    token = auth_svc.admin_login(payload.email, payload.password)
    if not token:
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": token}
