from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017/")
db = client["MobileLegend_wiki_backend"]
collection = db["itemInfo"]

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/items")
def get_all_items():
    items = list(collection.find())
    return [fix_id(item) for item in items]

@app.get("/items/name/{name}")
def get_item_by_name(name: str):
    item = collection.find_one({"ItemName": name})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return fix_id(item)

@app.get("/items/type/{type_name}")
def get_Items_by_type(type_name: str):
    items = list(collection.find({"Type": type_name}))
    if not items:
        raise HTTPException(status_code=404, detail=f"No Items found in type: {type_name}")
    return [fix_id(item) for item in items]





