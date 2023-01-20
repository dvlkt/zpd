import asyncio
import tornado.web

import data

class SetData(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write("")

class GetData(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(str({ "status": "Got it!" }))

async def run(): 
    api = tornado.web.Application([
        (r"/set", SetData),
		(r"/get", GetData),
    ])
    api.listen(1789)

    await asyncio.Event().wait()