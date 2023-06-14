import os, json
import data, algorithm

statistics = None
load_data = None

def save(file_path):
    if not os.path.exists(os.path.join(data.directory, "saves")):
        os.makedirs(os.path.join(data.directory, "saves"))
    
    data_file = open(os.path.join(data.directory, "saves", file_path), "w")
    data_file.write(json.dumps(algorithm.get_save_data()))
    data_file.close()

    statistics_file = open(os.path.join(data.directory, "saves", f"{file_path}_statistics"), "w")
    statistics_file.write("\n".join(statistics))
    statistics_file.close()

def load(file_path):
    global load_data

    algorithm.set_algorithm(algorithm.current_name)

    data_file = open(os.path.join(data.directory, "saves", file_path), "r")
    load_data = json.loads(str(data_file.read()))

    statistics_file = open(os.path.join(data.directory, "saves", f"{file_path}_statistics"), "r")
    statistics = statistics_file.read().split("\n")