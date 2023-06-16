import os, random

import config
import saving
import logging

current_name = None
current = None

hyperparameters = None
hyperparameter_values = None

available = []
for a in os.listdir(os.path.join(config.directory, "algorithms")):
    if a[-3:] == ".py" and a != "__init__.py":
        available.append(a[:-3])

def set_algorithm(value, default_value=None):
    global current_name, current, is_current_init, available, hyperparameters

    if not value in available:
        if current_name == None:
            set_algorithm(default_value)
        
        logging.warn(f"Nezināms algoritms: \"{value}\". Tiks izmantots \"{current_name}\".")
        return

    current_name = value
    current = __import__(f"algorithms.{current_name}", fromlist=["init", "update", "save"])

def get_save_data():
    if current != None:
        return current.save()
    else:
        return None

def adjust_hyperparameters():
    global hyperparameter_values

    hyperparameter_values = []
    for i in hyperparameters:
        hyperparameter_values.append(random.uniform(i[1], i[2]))