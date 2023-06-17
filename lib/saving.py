import os, json

import algo_handler
import config
import log
import game_handler.data
import graph_generator

loaded_state = None

def load():
    if config.input_file_name == None:
        return

    try:
        global loaded_state

        state_file = open(os.path.join(config.directory, "../data/", config.input_file_name + ".state.json"), "r")
        loaded_state = json.loads(str(state_file.read()))

        result_file = open(os.path.join(config.directory, "../data/", config.input_file_name + ".results.json"), "r")
        game_handler.data.results = json.loads(str(result_file.read()))

        log_file = open(os.path.join(config.directory, "../data/", config.input_file_name + ".log"), "r")
        log.file_log = str(log_file.read())

        hp_file = open(os.path.join(config.directory, "../data/", config.input_file_name + ".hp.json"), "r")
        algo_handler.hp.hyperparameters = json.loads(str(hp_file.read()))

        game_handler.data.played_episodes = len(game_handler.data.results)

        log.log(f"Dati ielādēti no \"{config.input_file_name}\"")
    except Exception as e:
        log.error(f"Nevarēja ielādēt datus (Vai visi nepieciešamie faili eksistē?): {e}")

def save():
    if config.output_file_name == None:
        return

    log.log("Saglabā datus...")

    try:
        if not os.path.exists(os.path.join(config.directory, "../data")):
            os.makedirs(os.path.join(config.directory, "../data"))
        
        state_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".state.json"), "w")
        state_file.write(json.dumps(algo_handler.get_save_data()))
        state_file.close()

        result_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".results.json"), "w")
        result_file.write(json.dumps(game_handler.data.results))
        result_file.close()

        log_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".log"), "w")
        log_file.write(log.file_log)
        log_file.close()

        hp_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".hp.json"), "w")
        hp_file.write(json.dumps(algo_handler.hp.hyperparameters))
        hp_file.close()

        graph_generator.generate_graph()

        log.log(f"Dati saglabāti ar nosaukumu \"{config.output_file_name}\"")
    except Exception as e:
        log.error(f"Nevarēja saglabāt datus: {e}")