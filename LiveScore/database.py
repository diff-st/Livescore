from pymongo import AsyncMongoClient
import os

class DBPool:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

        # Load configuration from environment variables
        self.mongo_host = os.getenv("MONGO_HOST", "localhost")
        self.mongo_port = int(os.getenv("MONGO_PORT", "27017"))
        self.mongo_user = os.getenv("MONGO_USER", "admin")
        self.mongo_password = os.getenv("MONGO_PASSWORD", "password")
        self.mongo_db = os.getenv("MONGO_DB", "users_db")
        self.mongo_collection = os.getenv("MONGO_DB_COLLECTION", "users")

    async def connect(self):
        DB_CONNECTION_STRING = f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"
        self.client = AsyncMongoClient(DB_CONNECTION_STRING,
                                       maxPoolSize = 20,
                                       minPoolSize = 5,
                                       maxIdleTimeMS = 30000)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]
        print("client connected to MongoDB service")

    async def close(self):
        if self.client:
            self.client.close()

    #------------------ CRUD methods ----------------------
    async def read_user_by_username(self, username: str):
        return await self.collection.find_one({"username" : username})

    async def create_user(self, username : str, password: str, email: str):
        user = await self.read_user_by_username(username)
        if not user:
            return await self.collection.insert_one({ "username" : username,
                                                "password" : password,
                                                "email" : email})
        return None







