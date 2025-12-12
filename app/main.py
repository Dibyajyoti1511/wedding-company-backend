from fastapi import FastAPI
from app.api.org_router import router as org_router
from app.api.admin_router import router as admin_router
from app.api.wedding_router import router as wedding_router
from app.config import settings

app = FastAPI(
    title="Wedding Company Organization Management Service",
    description="A comprehensive backend service for managing wedding companies with multi-tenant architecture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(org_router)
app.include_router(admin_router)
app.include_router(wedding_router)

@app.get("/")
def root():
    return {"message": "Wedding Company Service running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Wedding Company Management Service"} 
