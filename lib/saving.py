import os, json

import algorithm
import config
import logging
import game_handler.data

loaded_state = None

def load():
    if config.input_file_name == None:
        return

    try:
        global loaded_state

        algorithm.set_algorithm(algorithm.current_name)
        state_file = open(os.path.join(config.directory, "../data/", file_name + ".state.json"), "r")
        loaded_state = json.loads(str(state_file.read()))

        result_file = open(os.path.join(config.directory, "../data/", file_name + ".results.json"), "r")
        game_handler.data.results = json.loads(str(result_file.read()))

        game_handler.data.played_episodes = len(game_handler.data.results)

        logging.log(f"Dati ielādēti no {config.input_file_name}")
    except Exception as e:
        logging.error(f"Nevarēja ielādēt datus (Vai visi nepieciešamie faili eksistē?): {e}")

def save():
    if config.output_file_name == None:
        return

    logging.log("Saglabā datus...")

    try:
        if not os.path.exists(os.path.join(config.directory, "../data")):
            os.makedirs(os.path.join(config.directory, "../data"))
        
        state_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".state.json"), "w")
        state_file.write(json.dumps(algorithm.get_save_data()))
        state_file.close()

        result_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".results.json"), "w")
        result_file.write(json.dumps(game_handler.data.results))
        result_file.close()

        logging.log(f"Dati saglabāti ar nosaukumu {config.output_file_name}")
    except Exception as e:
        logging.error(f"Nevarēja saglabāt datus: {e}")