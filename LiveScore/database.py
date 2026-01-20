from pymongo import AsyncMongoClient
from bson import ObjectId
import os

class DBPool:
    def __init__(self):
        self.client = None
        self.db = None

        self.mongo_host = os.getenv("MONGO_HOST", "localhost")
        self.mongo_port = int(os.getenv("MONGO_PORT", "27017"))
        self.mongo_user = os.getenv("MONGO_USER", "admin")
        self.mongo_password = os.getenv("MONGO_PASSWORD", "password")
        self.mongo_db = os.getenv("MONGO_DB", "rugby_live")

    async def connect(self):
        uri = f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"
        self.client = AsyncMongoClient(uri)
        self.db = self.client[self.mongo_db]

        self.matches = self.db["matches"]
        self.events = self.db["events"]

        print("MongoDB connected")

    async def close(self):
        if self.client:
            self.client.close()

    # ---------- MATCHES ----------

    async def get_matches(self):
        cursor = self.matches.find()
        return [m async for m in cursor]

    async def get_match(self, match_id):
        return await self.matches.find_one({"_id": ObjectId(match_id)})

    async def create_match(self, home, away):
        return await self.matches.insert_one({
            "home_team": home,
            "away_team": away,
            "status": "scheduled",
            "minute": 0,
            "score": {"home": 0, "away": 0}
        })

    async def update_match(self, match_id, data):
        await self.matches.update_one(
            {"_id": ObjectId(match_id)},
            {"$set": data}
        )

    # ---------- EVENTS ----------

    async def add_event(self, match_id, event):
        event["match_id"] = ObjectId(match_id)
        await self.events.insert_one(event)

    async def get_events(self, match_id):
        cursor = self.events.find(
            {"match_id": ObjectId(match_id)}
        ).sort("minute", 1)
        return [e async for e in cursor]
