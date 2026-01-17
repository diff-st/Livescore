import tornado.ioloop
import tornado.web
from db import db_interface, PORT
from handlers import MatchesHandler, MatchDetailHandler
from ws import MatchWebSocket

def make_app():
    app = tornado.web.Application([
        (r"/api/matches", MatchesHandler),
        (r"/api/matches/([a-f0-9]+)", MatchDetailHandler),
        (r"/ws", MatchWebSocket),
    ])
    app.db = db_interface
    return app

if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
