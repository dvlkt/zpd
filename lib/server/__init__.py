from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import server.data as data
import server.body_parser as bp
import server.results as results
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

        is_ready = bp.is_ready()

        if is_ready and body.get("lost"):
            results.add(data.curr_score)
            data.played_episodes += 1
            saving.autosave()
        
        bp.parse(
            body.get("actionCount"),
            body.get("state"),
            body.get("score"),
            body.get("lost")
        )

        if not is_ready:
            try:
                self.wfile.write(bytes(json.dumps({
                    "action": -1
                }), "utf-8"))
            except Exception as e:
                log.error(f"Nevarēja atgriezt datus spēlei: {e}")
            return
        
        # Initialize if the algorithm hasn't been initialized yet
        if algorithm.learning_rate == None or algorithm.discount_factor == None:
            algorithm.hp_adjustment.adjust()
            
            log.log("Algoritms ir uzsākts un savienots ar spēli!")

        # Update the hyperparameters
        if data.played_episodes % config.episodes_per_hyperparameter == 0 and body.get("lost"):
            algorithm.reset()
            algorithm.hp_adjustment.adjust()
            
            hyperparameter_value_string = f"mācīšanās ātrums: {algorithm.learning_rate}, atlaides faktors: {algorithm.discount_factor}"
            log.verbose(f"Hiperparametri tika nomainīti ({hyperparameter_value_string}); {data.played_episodes}. epizode pabeigta")
        
        action = algorithm.update({ # This is where the magic happens
            "action_count": data.action_count,
            "state": data.curr_state,
            "score": data.curr_score,
            "lost": data.has_lost
        })
        
        try:
            self.wfile.write(bytes(json.dumps({
                "action": action
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