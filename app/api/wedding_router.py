from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import WeddingCreateSchema, WeddingUpdateSchema
from app.services.wedding_service import WeddingService
from app.utils.jwt_handler import JWTHandler
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/weddings", tags=["weddings"])
auth = HTTPBearer()

def get_wedding_service(token: HTTPAuthorizationCredentials = Depends(auth)) -> WeddingService:
    try:
        decoded = JWTHandler.decode_token(token.credentials)
        org_name = decoded.get("organization")
        return WeddingService(org_name)
    except Exception:
        raise HTTPException(401, "Invalid token")

@router.post("/")
def create_wedding(wedding: WeddingCreateSchema, svc: WeddingService = Depends(get_wedding_service)):
    try:
        return {"success": True, "data": svc.create_wedding(wedding)}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{wedding_id}")
def get_wedding(wedding_id: str, svc: WeddingService = Depends(get_wedding_service)):
    try:
        return {"success": True, "data": svc.get_wedding(wedding_id)}
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.put("/{wedding_id}")
def update_wedding(wedding_id: str, update: WeddingUpdateSchema, svc: WeddingService = Depends(get_wedding_service)):
    try:
        return {"success": True, "data": svc.update_wedding(wedding_id, update)}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/{wedding_id}")
def delete_wedding(wedding_id: str, svc: WeddingService = Depends(get_wedding_service)):
    try:
        return {"success": True, "data": svc.delete_wedding(wedding_id)}
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.get("/")
def list_weddings(svc: WeddingService = Depends(get_wedding_service)):
    return {"success": True, "data": svc.list_weddings()}
