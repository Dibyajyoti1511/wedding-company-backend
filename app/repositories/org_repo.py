from app.db import get_org_collection
from bson import ObjectId
from typing import List, Dict, Any

class OrgRepo:
    def __init__(self, org_name: str):
        self.collection = get_org_collection(org_name)
    
    def create_wedding(self, wedding_data: Dict[str, Any]) -> str:
        result = self.collection.insert_one(wedding_data)
        return str(result.inserted_id)
    
    def get_wedding(self, wedding_id: str) -> Dict[str, Any]:
        return self.collection.find_one({"_id": ObjectId(wedding_id)})
    
    def update_wedding(self, wedding_id: str, update_data: Dict[str, Any]) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(wedding_id)}, 
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_wedding(self, wedding_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(wedding_id)})
        return result.deleted_count > 0
    
    def list_weddings(self, org_name: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({"type": "wedding"}))
    