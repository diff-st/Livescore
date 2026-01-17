from bson import ObjectId

class DatabaseInterface:
    def __init__(self, db):
        self._matches = db["matches"]
        self._events = db["events"]

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
            "home_team": home,
            "away_team": away,
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
