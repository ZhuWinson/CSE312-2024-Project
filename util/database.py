import uuid
from pymongo import MongoClient

def create_record(collection, record):
    record_id = str(uuid.uuid4())
    record.setdefault("id", record_id)
    collection.insert_one(record)
    return record_id

def delete_record(collection, record_id):
    collection.delete_one({"id": record_id})

def list_records(collection):
    return list(collection.find({}, {"_id": False}))

def retrieve_record(collection, query):
    return collection.find_one(query, {"_id": False})

def update_record(collection, query, record):
    collection.update_one(query, {"$set": record})

client = MongoClient("mongo")
database = client["lmao"]
accounts = database["accounts"]
posts = database["posts"]