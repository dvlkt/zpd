from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import server.data as data
import algorithm
import algorithm.hp_adjustment
import saving
import log
import config

class Server(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        body_bin = self.rfile.read(int(self.headers["Content-Length"]))
        body = json.loads(body_bin.decode("utf-8"))

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        ### When losing ###
        if data.action_count != None and body.get("lost"):
            data.add_result(data.curr_score)
            data.played_episodes += 1
            saving.autosave()

        ### Handle action count ###
        if data.action_count == None and body.get("actionCount") != None:
            data.action_count = body.get("actionCount")
            log.verbose(f"Spēles darbību skaits iestatīts: {data.action_count}")
        
        if data.action_count == None: # Can't do anything before the action count is set
            try:
                self.wfile.write(bytes(json.dumps({
                    "action": -1,
                    "reset": False
                }), "utf-8"))
            except Exception as e:
                log.error(f"Nevarēja atgriezt datus spēlei: {e}")
            return
        
        ### Handle other fields ###
        if body.get("state") != None:
            data.curr_state = body.get("state")
        if body.get("score") != None:
            data.curr_score = body.get("score")
        if body.get("lost") != None:
            data.has_lost = body.get("lost")
        
        ### Update the hyperparameters ###
        needs_reset = False
        if algorithm.learning_rate == None or algorithm.discount_factor == None:
            needs_reset = True
        if data.played_episodes % config.episodes_per_hyperparameter == 0 and body.get("lost"):
            needs_reset = True
        
        if needs_reset:
            algorithm.reset()
            algorithm.hp_adjustment.adjust()
            
            hyperparameter_value_string = f"mācīšanās ātrums: {algorithm.learning_rate}, atlaides faktors: {algorithm.discount_factor}"
            log.verbose(f"Hiperparametri tika nomainīti ({hyperparameter_value_string}); {data.played_episodes}. epizode pabeigta")
        
        ### Return the action from the algorithm ###
        action = algorithm.update(data.action_count, data.curr_state, data.has_lost)
        try:
            self.wfile.write(bytes(json.dumps({
                "action": action,
                "reset": needs_reset
            }), "utf-8"))
        except Exception as e:
            log.error(f"Nevarēja atgriezt datus spēlei: {e}")


    def log_message(self, format, *args) -> None:
        pass # This is to disable logging in the console

def run() -> None:
    server = HTTPServer(("localhost", config.port), Server)
    log.log(f"API serveris pieejams šeit: http://localhost:{config.port}")

    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.error(e)

    server.server_close()
    log.log("API serveris tika aizvērts.")