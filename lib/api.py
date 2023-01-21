import asyncio
import tornado.web

import data

class SetData(tornado.web.RequestHandler):
	def post(self):
		error = ""

		self.set_header("Content-Type", "application/json")
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write({ "error": error })

class GetData(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "application/json")
		self.set_header("Access-Control-Allow-Origin", "*")

		self.write({

		})

async def run(): 
	api = tornado.web.Application([
		(r"/set", SetData),
		(r"/get", GetData),
	])
	api.listen(1789)

	await asyncio.Event().wait()