import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoManager:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("MONGO_DB")
        self.collection_name = os.getenv("MONGO_COLLECTION")
        
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def salvar_analise(self, dados):
        query = {"arquivo": dados.get("arquivo")}
        update = {"$set": dados}
        result = self.collection.update_one(query, update, upsert=True)
        return result.upserted_id or "Atualizado"