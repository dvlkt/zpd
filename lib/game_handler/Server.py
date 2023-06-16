from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import game_handler.data as data
import game_handler.body_parser as bp
import game_handler.results as results
import algorithm
import saving
import logging

class Server(BaseHTTPRequestHandler):
    port = 1789

    def do_POST(self) -> None:
        body_bin = self.rfile.read(int(self.headers["Content-Length"]))

        body = json.loads(body_bin.decode("utf-8"))

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if body.get("lost"):
            results.add(data.curr_score)
            data.played_episodes += 1
        
        is_ready = bp.parse(
            body.get("title"),
            body.get("stateSize"),
            body.get("actionCount"),
            body.get("state"),
            body.get("score"),
            body.get("lost")
        )

        if is_ready:
            # Initialize if the algorithm hasn't been initialized yet
            if algorithm.hyperparameters == None:
                try:
                    algorithm.hyperparameters = algorithm.current.init({
                        "action_count": data.action_count,
                        "state_size": data.state_size
                    }, saving.loaded_state)
                except Exception as e:
                    logging.error(f"Nevarēja uzsākt algoritmu: {e}")
                
                logging.log("Algoritms ir uzsākts!")
                logging.log(f"Savienots ar spēli: {data.title}")

            # Update the hyperparameters
            algorithm.adjust_hyperparameters()
            
            action = -1
            try:
                action = algorithm.current.update({ # This is where the magic happens
                    "action_count": data.action_count,
                    "state_size": data.state_size,
                    "state": data.curr_state,
                    "score": data.curr_score,
                    "lost": data.has_lost
                }, algorithm.hyperparameter_values)
            except Exception as e:
                logging.error(f"Nevarēja atjaunot algoritmu: {e}")
            
            try:
                self.wfile.write(bytes(json.dumps({
                    "action": action
                }), "utf-8"))
            except Exception as e:
                logging.error(f"Nevarēja atgriezt datus spēlei: {e}")
        else:
            try:
                self.wfile.write(bytes(json.dumps({
                    "action": -1
                }), "utf-8"))
            except Exception as e:
                logging.error(f"Nevarēja atgriezt datus spēlei: {e}")


    def log_message(self, format, *args) -> None:
        pass # This is to disable logging in the console