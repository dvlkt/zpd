import random

import config
import algorithm

step = 0
pos = None
used_positions = []

def adjust() -> None:
    global step, pos, used_positions

    if pos == None:
        pos = [0, 0]

    algorithm.learning_rate = pos[0]
    algorithm.discount_factor = pos[1]
    used_positions.append(tuple(pos))

    while True:
        i = 0
        while i < 2:
            if pos[i] >= 1:
                pos[i] = 0
                i += 1
                continue
            
            pos[i] += 1 / 2 ** step
            break
        else:
            # If all HPs == 1, enter the next step
            step += 1
            pos = [0, 0]

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