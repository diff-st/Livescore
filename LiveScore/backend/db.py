from pymongo import AsyncMongoClient
from .db_interface import DatabaseInterface

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "rugby_live"

PORT = 8888
COOKIE_SECRET = "change_me"

client = AsyncMongoClient(MONGO_URL)
db = client[DB_NAME]

db_interface = DatabaseInterface(db)
