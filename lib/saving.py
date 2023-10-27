import os, json

import algorithm
import algorithm.hp_adjustment
import config
import log
import server.data
import graph_generator

def load():
    if config.input_file_name == None:
        return

    try:
        data_file = open(os.path.join(config.directory, "../data/", config.input_file_name + ".json"), "r")
        load_data = json.loads(str(data_file.read()))

        algorithm.q_table = load_data["q_table"]

        algorithm.learning_rate = load_data["hyperparameters"]["learning_rate"]
        algorithm.discount_factor = load_data["hyperparameters"]["discount_factor"]

        algorithm.hp_adjustment.step = load_data["hyperparameters"]["grid"]["step"]
        algorithm.hp_adjustment.pos = load_data["hyperparameters"]["grid"]["pos"]
        algorithm.hp_adjustment.used = load_data["hyperparameters"]["grid"]["used"]

        server.data.played_episodes = load_data["game_data"]["played_episodes"]
        server.data.results = load_data["game_data"]["results"]

        log_file = open(os.path.join(config.directory, "../data/", config.input_file_name + ".log"), "r")
        log.file_log = str(log_file.read())

        log.log(f"Dati ielādēti no \"{config.input_file_name}\"")
    except Exception as e:
        log.error(f"Nevarēja ielādēt datus (Vai visi nepieciešamie faili eksistē?): {e}")

def save(is_autosave=False):
    if config.output_file_name == None:
        return
    
    if not is_autosave:
        log.log("Saglabā datus...")
    
    try:
        if not os.path.exists(os.path.join(config.directory, "../data")):
            os.makedirs(os.path.join(config.directory, "../data"))
        
        save_data = {
            "q_table": algorithm.q_table,
            "hyperparameters": {
                "learning_rate": algorithm.learning_rate,
                "discount_factor": algorithm.discount_factor,
                "grid": {
                    "step": algorithm.hp_adjustment.step,
                    "pos": algorithm.hp_adjustment.pos,
                    "used": algorithm.hp_adjustment.used_positions
                }
            },
            "game_data": {
                "played_episodes": server.data.played_episodes,
                "results": server.data.results
            }
        }
        data_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".json"), "w")
        data_file.write(json.dumps(save_data))
        data_file.close()

        log_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".log"), "w")
        log_file.write(log.file_log)
        log_file.close()

        generated_graph = graph_generator.generate_graph(is_silent=is_autosave)
        if generated_graph != None:
            generated_graph.savefig(os.path.join(config.directory, "../data/", config.output_file_name + ".png"))

        if not is_autosave:
            log.log(f"Dati saglabāti ar nosaukumu \"{config.output_file_name}\"")
        else:
            log.verbose(f"Dati saglabāti")
    except Exception as e:
        log.error(f"Nevarēja saglabāt datus: {e}")

def autosave():
    if config.autosave_interval != None and server.data.played_episodes % config.autosave_interval == 0:
        save(is_autosave=True)