import os, json

import algorithm
import game_handler.data

results = None
loaded_state = None

def load(file_name):
    try:
        global loaded_state

        algorithm.set_algorithm(algorithm.current_name)
        state_file = open(os.path.join(config.directory, "../data/", file_name + ".state.json"), "r")
        loaded_state = json.loads(str(state_file.read()))

        result_file = open(os.path.join(config.directory, "../data/", file_name + ".results.json"), "r")
        results = json.loads(str(result_file.read()))

        game_handler.data.played_episodes = len(results)

        return True
    except:
        return False

def save(file_name):
    try:
        if not os.path.exists(os.path.join(config.directory, "../data")):
            os.makedirs(os.path.join(config.directory, "../data"))
        
        state_file = open(os.path.join(config.directory, "../data/", file_name + ".state.json"), "w")
        state_file.write(json.dumps(algorithm.get_save_data()))
        state_file.close()

        result_file = open(os.path.join(config.directory, "../data/", file_name + ".results.json"), "w")
        result_file.write(json.dumps(results))
        result_file.close()

        return True
    except:
        return False

def add_result(score):
    hyperparameter_obj = {}
    for i in range(len(algorithm.hyperparameters)):
        hyperparameter_obj[algorithm.hyperparameters[i][0]] = algorithm.hyperparameter_values[i]

    results.append({
        "hyperparameters": hyperparameter_obj,
        "score": str(config.game_score)
    })