import asyncio
import tornado.web
import tornado.escape
import signal

from database import DBPool

class APIHandler(tornado.web.RequestHandler):
    def initialize(self, db_pool):
        self.db_pool = db_pool

    async def get(self):
        self.set_header("Content-Type", "application/json")

        username = self.get_query_argument("username", None)
        if not username:
            self.set_status(400)
            self.write({"error": "user not specified"})
            return

        result = await self.db_pool.read_user_by_username(username)
        if result:
            self.set_status(200)
            response_body = {"id" : str(result["_id"]),
                             "username" : result["username"],
                             "email" : result["email"]}
            self.write(response_body)
        else:
            self.set_status(404)
            self.write({"error" : "user not found"})

    async def post(self):
        self.set_header("Content-Type", "application/json")

        input_data = tornado.escape.json_decode(self.request.body)
        username = input_data["username"]
        password = input_data["password"]
        email = input_data["email"]

        if not all([username, password, email]):
            self.set_status(400)
            self.write({"error": "username, password and email are required"})
            return

        result = await self.db_pool.create_user(username, password, email)

        if result:
            self.set_status(201)
            self.write({"message" : "new user created",
                        "id" : str(result.inserted_id)})
        else:
            self.set_status(409)
            self.write({"error" : "user already exist"})


def make_app(db_pool):
    """Create the Tornado application with the shared pool"""
    return tornado.web.Application([
        (r"/api/users", APIHandler, dict(db_pool = db_pool))
    ])

async def main():
    db_pool = DBPool()
    await db_pool.connect()

    app = make_app(db_pool)
    app.listen(8888)
    print("server listening on port 8888")

    shutdown_event = asyncio.Event()

    def signal_handler(signum, frame):
        print("\nshutting down server gracefully")
        shutdown_event.set()

    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await shutdown_event.wait()
    finally:
        await db_pool.close()
        print("\nserver stopped")

asyncio.run(main())