from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import game_handler.data as data
import game_handler.body_parser as bp
import game_handler.results as results
import algo_handler
import algo_handler.hp
import algo_handler.hp_adjustment
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
            body.get("title"),
            body.get("stateSize"),
            body.get("actionCount"),
            body.get("state"),
            body.get("score"),
            body.get("lost")
        )

        if is_ready:
            # Initialize if the algorithm hasn't been initialized yet
            if algo_handler.hp.hyperparameters == None:

                try:
                    hyperparameters = algo_handler.current.init({
                        "action_count": data.action_count,
                        "state_size": data.state_size
                    }, saving.loaded_state)

                    algo_handler.hp.init(hyperparameters)

                    algo_handler.hp_adjustment.adjust()

                except Exception as e:
                    log.error(f"Nevarēja uzsākt algoritmu: {e}")
                
                log.log("Algoritms ir uzsākts!")
                log.log(f"Savienots ar spēli: {data.title}")

            # Update the hyperparameters
            updated_hyperparameters = None
            if data.played_episodes % config.episodes_per_hyperparameter == 0 and body.get("lost") and config.hp_adjustment_strategy != "default":
                algo_handler.hp_adjustment.adjust()
                updated_hyperparameters = algo_handler.hp.get_values()
                
                hyperparameter_value_string = ", ".join([f"{i['name']}: {i['value']}" for i in algo_handler.hp.hyperparameters])
                log.verbose(f"Hiperparametri tika nomainīti ({hyperparameter_value_string}); {data.played_episodes}. epizode pabeigta")
            
            action = -1
            try:
                action = algo_handler.current.update({ # This is where the magic happens
                    "action_count": data.action_count,
                    "state_size": data.state_size,
                    "state": data.curr_state,
                    "score": data.curr_score,
                    "lost": data.has_lost
                }, updated_hyperparameters)
            except Exception as e:
                log.error(f"Nevarēja atjaunot algoritmu: {e}")
            
            try:
                self.wfile.write(bytes(json.dumps({
                    "action": action
                }), "utf-8"))
            except Exception as e:
                log.error(f"Nevarēja atgriezt datus spēlei: {e}")
        else:
            try:
                self.wfile.write(bytes(json.dumps({
                    "action": -1
                }), "utf-8"))
            except Exception as e:
                log.error(f"Nevarēja atgriezt datus spēlei: {e}")


    def log_message(self, format, *args) -> None:
        pass # This is to disable logging in the console