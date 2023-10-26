import random

import config
import algo_handler.hp as hp

step = 0
pos = None
used_positions = []

def adjust() -> None:
    global step, pos, used_positions

    if hp.hyperparameters == None:
        return
    if pos == None:
        pos = [0 for i in range(len(hp.hyperparameters))]

    for h in range(len(hp.hyperparameters)):
        min_v = hp.hyperparameters[h]["min"]
        max_v = hp.hyperparameters[h]["max"]
        hp.hyperparameters[h]["value"] = pos[h] * (max_v - min_v) + min_v
    used_positions.append(tuple(pos))

    while True:
        i = 0
        while i < len(hp.hyperparameters):
            if pos[i] >= 1:
                pos[i] = 0
                i += 1
                continue
            
            pos[i] += 1 / 2 ** step
            break
        else:
            # If all HPs == 1, enter the next step
            step += 1
            pos = [0 for o in range(len(hp.hyperparameters))]

        if not tuple(pos) in used_positions:
            break

def load(data) -> None:
    global step, pos, used_positions

    step = int(data["step"])
    pos = data["pos"]
    used_positions = data["used"]

def save() -> dict:
    global step, pos, used_positions

    return {
        "step": step,
        "pos": pos,
        "used": used_positions
    }