import tornado.web
import json

class MatchesHandler(tornado.web.RequestHandler):
    async def get(self):
        matches = await self.application.db.get_all_matches()
        self.write(json.dumps(matches, default=str))

class MatchDetailHandler(tornado.web.RequestHandler):
    async def get(self, match_id):
        match = await self.application.db.get_match(match_id)
        events = await self.application.db.get_events_by_match(match_id)
        self.write(json.dumps({
            "match": match,
            "events": events
        }, default=str))
