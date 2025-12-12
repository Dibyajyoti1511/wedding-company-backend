from app.db import master_db
from bson import ObjectId

class MasterRepo:
    def __init__(self):
        self.orgs = master_db["orgs"]
        self.admins = master_db["admins"]

    def find_org(self, organization_name: str):
        return self.orgs.find_one({"organization_name": organization_name})

    def create_org_record(self, organization_name: str, collection_name: str, admin_id):
        return self.orgs.insert_one({
            "organization_name": organization_name,
            "collection_name": collection_name,
            "admin_id": ObjectId(admin_id)
        })

    def delete_org(self, organization_name: str):
        return self.orgs.delete_one({"organization_name": organization_name})

    # Admins
    def create_admin(self, email: str, hashed_password: str, organization_name: str):
        res = self.admins.insert_one({
            "email": email,
            "password": hashed_password,
            "organization": organization_name
        })
        return res.inserted_id

    def find_admin_by_email(self, email: str):
        return self.admins.find_one({"email": email})

    def delete_admin_by_org(self, organization_name: str):
        return self.admins.delete_many({"organization": organization_name})

    def update_admin_by_org(self, organization_name: str, update_fields: dict):
        return self.admins.update_one({"organization": organization_name}, {"$set": update_fields})
