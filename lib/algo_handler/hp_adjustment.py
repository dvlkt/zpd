import random

import config
import algo_handler.hp as hp

def __random_adjust() -> None:
    for h in hp.hyperparameters:
        h["value"] = random.uniform(h["min"], h["max"])


grid_step = 0
grid_pos = None
used_positions = []
def __grid_adjust() -> None:
    global grid_step, grid_pos, used_positions

    if hp.hyperparameters == None:
        return
    if grid_pos == None:
        grid_pos = [0 for i in range(len(hp.hyperparameters))]

    for h in range(len(hp.hyperparameters)):
        min_v = hp.hyperparameters[h]["min"]
        max_v = hp.hyperparameters[h]["max"]
        hp.hyperparameters[h]["value"] = grid_pos[h] * (max_v - min_v) + min_v
    used_positions.append(tuple(grid_pos))

    while True:
        i = 0
        while i < len(hp.hyperparameters):
            if grid_pos[i] >= 1:
                grid_pos[i] = 0
                i += 1
                continue
            
            grid_pos[i] += 1 / 2 ** grid_step
            break
        else:
            # If all HPs == 1, enter the next step
            grid_step += 1
            grid_pos = [0 for o in range(len(hp.hyperparameters))]

        if not tuple(grid_pos) in used_positions:
            break


def adjust() -> None:
    if config.hp_adjustment_strategy == "grid":
        __grid_adjust()
    elif config.hp_adjustment_strategy == "random":
        __random_adjust()