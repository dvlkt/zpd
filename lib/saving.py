import os, json

import algorithm
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
        algorithm.hp.hyperparameters = json.loads(str(hp_file.read()))

        has_file = open(os.path.join(config.directory, "../data/", config.input_file_name + ".grid.json"), "r")
        algorithm.hp_adjustment.load(json.loads(str(has_file.read())))

        game_handler.data.played_episodes = 0
        for i in game_handler.data.results:
            game_handler.data.played_episodes += len(i["scores"])

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
        
        state_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".state.json"), "w")
        state_file.write(json.dumps(algorithm.save()))
        state_file.close()

        result_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".results.json"), "w")
        result_file.write(json.dumps(game_handler.data.results))
        result_file.close()

        log_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".log"), "w")
        log_file.write(log.file_log)
        log_file.close()

        hp_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".hp.json"), "w")
        hp_file.write(json.dumps(algorithm.hp.hyperparameters))
        hp_file.close()
        
        has_file = open(os.path.join(config.directory, "../data/", config.output_file_name + ".grid.json"), "w")
        has_file.write(json.dumps(algorithm.hp_adjustment.save()))
        has_file.close()

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
    if config.autosave_interval != None and game_handler.data.played_episodes % config.autosave_interval == 0:
        save(is_autosave=True)