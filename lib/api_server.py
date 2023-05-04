import json, random
from http.server import BaseHTTPRequestHandler, HTTPServer
import data, algorithm, saving

PORT = 1789

class Server(BaseHTTPRequestHandler):
    def do_POST(self):
        body_bin = self.rfile.read(int(self.headers['Content-Length']))

        body = json.loads(body_bin.decode("utf-8"))

        ## Parse received data ##
        if body.get("reset") != None:
            data.set_game_view_dimensions(None)
            data.set_game_title(None)
            data.set_game_action_count(None)
            data.set_game_view(None)
            data.set_initialized(False)
        
        if body.get("viewDimensions") != None:
            if data.game_view_dimensions == None:
                data.set_game_view_dimensions((body["viewDimensions"][0], body["viewDimensions"][1]))
        if body.get("title") != None:
            if data.game_title == None:
                data.set_game_title(body["title"])
        if body.get("actionCount") != None:
            if data.game_action_count == None:
                data.set_game_action_count(body["actionCount"])

        has_lost = False
        if data.game_view_dimensions != None and data.game_title != None and data.game_action_count != None:
            if not algorithm.is_initialized:
                algorithm.current.init({
                    "action_count": data.game_action_count,
                    "view_dimensions": data.game_view_dimensions
                }, saving.load_data)
                algorithm.set_initialized()

            if body.get("view") != None:
                data.set_game_view(body["view"])
            if body.get("score") != None:
                data.set_game_score(body["score"])
            if body.get("lost") != None and body["lost"]:
                has_lost = True

        ## Return data ##
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        action = algorithm.current.update({ # This is where the magic happens
            "action_count": data.game_action_count,
            "view_dimensions": data.game_view_dimensions,
            "view": data.game_view,
            "score": data.game_score,
            "lost": has_lost
        })

        self.wfile.write(bytes(json.dumps({
            "action": action
        }), "utf-8"))
    

    def log_message(self, format, *args):
        pass # This is to disable logging in the console