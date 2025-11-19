import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[MongoClient] = None
_db = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(DATABASE_URL)
    return _client


def get_db():
    global _db
    if _db is None:
        _db = get_client()[DATABASE_NAME]
    return _db


def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    db = get_db()
    now = datetime.utcnow()
    doc = {**data, "created_at": now, "updated_at": now}
    result = db[collection_name].insert_one(doc)
    return str(result.inserted_id)


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    docs: List[Dict[str, Any]] = []
    for d in cursor:
        d["_id"] = str(d["_id"])  # convert ObjectId to string
        docs.append(d)
    return docs
