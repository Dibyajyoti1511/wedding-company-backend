from pymongo import MongoClient
from app.config import settings

_client = MongoClient(settings.MONGO_URI)
master_db = _client[settings.MASTER_DB_NAME]

def get_org_collection(org_name: str):
    """
    Return a reference to collection 'data' in database org_<org_name>.
    """
    db_name = f"org_{org_name}"
    return _client[db_name]["data"]

def drop_org_database(org_name: str):
    db_name = f"org_{org_name}"
    _client.drop_database(db_name)
