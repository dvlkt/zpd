import os, json
import data, algorithm

results = None
loaded_state = None

def load_state(file_path):
    try:
        global loaded_state

        algorithm.set_algorithm(algorithm.current_name)

        state_file = open(os.path.join(data.directory, "../", file_path), "r")
        loaded_state = json.loads(str(state_file.read()))

        return True
    except:
        return False

def save_state(file_path):
    try:
        state_file = open(os.path.join(data.directory, "../", file_path), "w")
        state_file.write(json.dumps(algorithm.get_save_data()))
        state_file.close()

        return True
    except:
        return False

def save_results(file_path):
    try:
        result_file = open(os.path.join(data.directory, "../", file_path), "w")
        result_file.write(json.dumps(results))
        result_file.close()

        return True
    except:
        return False