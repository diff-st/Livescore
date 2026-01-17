import tornado.websocket
import json

clients = set()

class MatchWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.add(self)

    def on_close(self):
        clients.remove(self)

def broadcast(match):
    message = json.dumps({
        "type": "match_update",
        "data": match
    })
    for c in clients:
        c.write_message(message)
