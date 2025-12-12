from pydantic import BaseModel, EmailStr

class OrgCreateSchema(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrgUpdateSchema(BaseModel):
    organization_name: str
    new_organization_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class OrgGetSchema(BaseModel):
    organization_name: str

class AdminLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str

class WeddingCreateSchema(BaseModel):
    bride_name: str
    groom_name: str
    wedding_date: str  # ISO format
    venue: str
    budget: float | None = None

class WeddingUpdateSchema(BaseModel):
    bride_name: str | None = None
    groom_name: str | None = None
    wedding_date: str | None = None
    venue: str | None = None
    budget: float | None = None

class WeddingSchema(WeddingCreateSchema):
    id: str
    organization_name: str
