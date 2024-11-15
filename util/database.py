import uuid
from pymongo import MongoClient

def create_record(collection, record):
    record_id = str(uuid.uuid4())
    record.setdefault("id", record_id)
    collection.insert_one(record)
    return record_id

def delete_record(collection, query):
    collection.delete_one(query)

def list_records(collection, query={}):
    return list(collection.find(query, {"_id": False}))

def retrieve_record(collection, query):
    return collection.find_one(query, {"_id": False})

def update_record(collection, query, record):
    collection.update_one(query, {"$set": record})

client = MongoClient("mongo")
database = client["lmao"]
accounts = database["accounts"]
posts = database["posts"]