from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import OrgCreateSchema, OrgGetSchema, OrgUpdateSchema
from app.services.org_service import OrgService
from app.utils.jwt_handler import JWTHandler
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/org", tags=["org"])
org_svc = OrgService()
auth = HTTPBearer()

@router.post("/create")
def create_org(payload: OrgCreateSchema):
    try:
        res = org_svc.create_org(payload.organization_name, payload.email, payload.password)
        return {"success": True, "data": res}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/get")
def get_org(organization_name: str):
    rec = org_svc.get_org(organization_name)
    if not rec:
        raise HTTPException(404, "Organization not found")
    # return sanitized metadata
    rec.pop("_id", None)
    return {"success": True, "data": rec}

@router.put("/update")
def update_org(payload: OrgUpdateSchema, token: HTTPAuthorizationCredentials = Depends(auth)):
    # Only an authenticated admin may update; validate token
    try:
        decoded = JWTHandler.decode_token(token.credentials)
    except Exception:
        raise HTTPException(401, "Invalid token")
    # only allow admin of the organization
    if decoded.get("organization") != payload.organization_name:
        raise HTTPException(403, "Not authorized to modify this organization")
    try:
        res = org_svc.update_org(payload.organization_name, payload.email, payload.password, payload.new_organization_name)
        return {"success": True, "data": res}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/delete")
def delete_org(organization_name: str, token: HTTPAuthorizationCredentials = Depends(auth)):
    try:
        decoded = JWTHandler.decode_token(token.credentials)
    except Exception:
        raise HTTPException(401, "Invalid token")
    if decoded.get("organization") != organization_name:
        raise HTTPException(403, "Not authorized to delete this organization")
    try:
        res = org_svc.delete_org(organization_name)
        return {"success": True, "data": res}
    except ValueError as e:
        raise HTTPException(400, str(e))
