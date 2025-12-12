from app.repositories.master_repo import MasterRepo
from app.db import get_org_collection, drop_org_database
from app.utils.hashing import Hasher

class OrgService:
    def __init__(self):
        self.repo = MasterRepo()

    def create_org(self, organization_name: str, email: str, password: str) -> dict:
        # Validate uniqueness
        if self.repo.find_org(organization_name):
            raise ValueError("Organization already exists")

        # Create dynamic collection (implicit on first insert or explicitly)
        coll = get_org_collection(organization_name)
        # Optionally initialize with a doc or index
        coll.insert_one({"_meta": {"created_at": __import__("datetime").datetime.utcnow()}})

        # Create admin
        hashed = Hasher.hash_password(password)
        admin_id = self.repo.create_admin(email, hashed, organization_name)

        # Store master record
        collection_name = f"org_{organization_name}"
        self.repo.create_org_record(organization_name, collection_name, admin_id)

        return {
            "organization_name": organization_name,
            "collection_name": collection_name,
            "admin_id": str(admin_id)
        }

    def get_org(self, organization_name: str):
        record = self.repo.find_org(organization_name)
        return record

    def update_org(self, organization_name: str, email: str | None, password: str | None, new_organization_name: str | None = None):
        # Check current organization exists
        rec = self.repo.find_org(organization_name)
        if not rec:
            raise ValueError("Organization not found")

        # If renaming organization: ensure no conflicts and handle collection rename by copying
        if new_organization_name and new_organization_name != organization_name:
            if self.repo.find_org(new_organization_name):
                raise ValueError("New organization name already exists")

            # Copy existing data to new db/collection
            old_coll = get_org_collection(organization_name)
            new_coll = get_org_collection(new_organization_name)

            # stream copy (simple)
            docs = old_coll.find({})
            batch = []
            for d in docs:
                if "_id" in d:
                    d.pop("_id")
                batch.append(d)
                if len(batch) >= 500:
                    new_coll.insert_many(batch); batch = []
            if batch:
                new_coll.insert_many(batch)

            # Update master repo record
            self.repo.orgs.update_one(
                {"organization_name": organization_name},
                {"$set": {
                    "organization_name": new_organization_name,
                    "collection_name": f"org_{new_organization_name}"
                }}
            )

            # update admin's organization field
            self.repo.admins.update_many({"organization": organization_name}, {"$set": {"organization": new_organization_name}})

            # drop old db
            drop_org_database(organization_name)
            organization_name = new_organization_name

        # update admin fields if provided
        update_fields = {}
        if email:
            update_fields["email"] = email
        if password:
            update_fields["password"] = Hasher.hash_password(password)
        if update_fields:
            self.repo.update_admin_by_org(organization_name, update_fields)

        return {"message": "Organization updated", "organization_name": organization_name}

    def delete_org(self, organization_name: str):
        rec = self.repo.find_org(organization_name)
        if not rec:
            raise ValueError("Organization not found")
        # delete dynamic data
        drop_org_database(organization_name)
        # delete master & admins
        self.repo.delete_org(organization_name)
        self.repo.delete_admin_by_org(organization_name)
        return {"message": "Organization deleted"}
