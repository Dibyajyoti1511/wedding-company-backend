from app.repositories.org_repo import OrgRepo
from app.models.schemas import WeddingCreateSchema, WeddingUpdateSchema
from typing import Dict, Any, List

class WeddingService:
    def __init__(self, org_name: str):
        self.repo = OrgRepo(org_name)
        self.org_name = org_name
    
    def create_wedding(self, wedding_data: WeddingCreateSchema) -> Dict[str, Any]:
        data = wedding_data.dict()
        data["type"] = "wedding"
        data["organization"] = self.org_name
        wedding_id = self.repo.create_wedding(data)
        return {"id": wedding_id, **data}
    
    def get_wedding(self, wedding_id: str) -> Dict[str, Any]:
        wedding = self.repo.get_wedding(wedding_id)
        if not wedding:
            raise ValueError("Wedding not found")
        wedding["id"] = str(wedding["_id"])
        wedding.pop("_id")
        return wedding
    
    def update_wedding(self, wedding_id: str, update_data: WeddingUpdateSchema) -> Dict[str, Any]:
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        if not self.repo.update_wedding(wedding_id, update_dict):
            raise ValueError("Wedding not found or no changes made")
        return self.get_wedding(wedding_id)
    
    def delete_wedding(self, wedding_id: str) -> Dict[str, str]:
        if not self.repo.delete_wedding(wedding_id):
            raise ValueError("Wedding not found")
        return {"message": "Wedding deleted"}
    
    def list_weddings(self) -> List[Dict[str, Any]]:
        weddings = self.repo.list_weddings(self.org_name)
        for wedding in weddings:
            wedding["id"] = str(wedding["_id"])
            wedding.pop("_id")
        return weddings
    