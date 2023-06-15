import json, random
from http.server import BaseHTTPRequestHandler, HTTPServer

import data
import algorithm
import saving

PORT = 1789

current_episode = 0

class Server(BaseHTTPRequestHandler):
    def do_POST(self):
        global current_episode

        body_bin = self.rfile.read(int(self.headers["Content-Length"]))

        body = json.loads(body_bin.decode("utf-8"))

        ## Parse received data ##
        if body.get("reset") != None:
            data.game_state_size = None
            data.game_title = None
            data.game_action_count = None
            data.game_state = None
            algorithm.hyperparameters = None
            saving.results = None
            current_episode = 0

        if body.get("stateSize") != None:
            if data.game_state_size == None:
                data.game_state_size = body["stateSize"]
        if body.get("title") != None:
            if data.game_title == None:
                data.game_title = body["title"]
        if body.get("actionCount") != None:
            if data.game_action_count == None:
                data.game_action_count = body["actionCount"]

        has_lost = False
        if data.game_state_size != None and data.game_title != None and data.game_action_count != None:
            if algorithm.hyperparameters == None:
                algorithm.hyperparameters = algorithm.current.init({
                    "action_count": data.game_action_count,
                    "state_size": data.game_state_size
                }, saving.loaded_state)

            if body.get("state") != None:
                data.game_state = body["state"]
            if body.get("score") != None:
                data.game_score = body["score"]
            if body.get("lost") != None and body["lost"]:
                has_lost = True
                current_episode += 1
        
        if saving.results == None:
            saving.results = []
        if has_lost:
            saving.results.append(str(data.game_score))

        ## Adjust hyperparameters
        if algorithm.hyperparameters != None:
            if current_episode % data.episodes_per_hyperparameter == 0:
                algorithm.adjust_hyperparameters()

        ## Return data ##
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if data.game_action_count != None and data.game_state_size != None and data.game_state != None and data.game_score != None and algorithm.hyperparameters != None:
            action = algorithm.current.update({ # This is where the magic happens
                "action_count": data.game_action_count,
                "state_size": data.game_state_size,
                "state": data.game_state,
                "score": data.game_score,
                "lost": has_lost
            }, algorithm.hyperparameter_values)

            self.wfile.write(bytes(json.dumps({
                "action": action
            }), "utf-8"))
        else:
            self.wfile.write(bytes(json.dumps({
                "action": -1
            }), "utf-8"))
    

    def log_message(self, format, *args):
        pass # This is to disable logging in the console