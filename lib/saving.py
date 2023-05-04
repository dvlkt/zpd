import os, json
import data, algorithm

load_data = None

def save(file_path):
    if not os.path.exists(os.path.join(data.directory, "saves")):
        os.makedirs(os.path.join(data.directory, "saves"))
    
    file = open(os.path.join(data.directory, "saves", file_path), "w")
    file.write(json.dumps(algorithm.get_save_data()))
    file.close()

def load(file_path):
    global load_data
    file = open(os.path.join(data.directory, "saves", file_path), "r")
    load_data = json.loads(str(file.read()))
    algorithm.set_algorithm(algorithm.current_name)