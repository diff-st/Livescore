from bson import ObjectId
import json
import os

class DatabaseInterface:
    def __init__(self, db):
        self._db = db

        self._teams = db["teams"]
        self._players = db["players"]
        self._matches = db["matches"]
        self._events = db["events"]


    # JSON

    async def load_initial_data(self):
        if await self._teams.count_documents({}) == 0:
            await self._load_json("data/teams.json", self._teams)

        if await self._players.count_documents({}) == 0:
            await self._load_json("data/players.json", self._players)

    async def _load_json(self, path, collection):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data:
            await collection.insert_many(data)

    # TEAMS

    async def get_teams(self):
        cursor = self._teams.find()
        return [t async for t in cursor]

    async def get_team_by_code(self, code: str):
        return await self._teams.find_one({"code": code})

    # PLAYERS

    async def get_players_by_team(self, team_code: str):
        cursor = self._players.find({"team": team_code})
        return [p async for p in cursor]

    # MATCHES

    async def get_all_matches(self):
        cursor = self._matches.find()
        return [m async for m in cursor]

    async def get_match(self, match_id: str):
        return await self._matches.find_one(
            {"_id": ObjectId(match_id)}
        )

    async def create_match(self, home: str, away: str):
        return await self._matches.insert_one({
            "home_team": home,     # team code (es. "NZ")
            "away_team": away,     # team code
            "status": "scheduled",
            "minute": 0,
            "score": {"home": 0, "away": 0}
        })

    async def update_match(self, match_id: str, data: dict):
        return await self._matches.update_one(
            {"_id": ObjectId(match_id)},
            {"$set": data}
        )

    # EVENTS

    async def add_event(self, match_id: str, event: dict):
        event["match_id"] = ObjectId(match_id)
        return await self._events.insert_one(event)

    async def get_events_by_match(self, match_id: str):
        cursor = self._events.find(
            {"match_id": ObjectId(match_id)}
        ).sort("minute", 1)
        return [e async for e in cursor]
