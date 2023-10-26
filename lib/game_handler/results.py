import numpy as np

import game_handler.data as data
import algorithm.hp

def add(score: int) -> None:
    hp_values = algorithm.hp.get_named_values()

    new_hyperparameters: bool = False
    if len(data.results) == 0:
        new_hyperparameters = True
    else:
        # Check if the current hyperparameters match the ones used in the last thing saved in results
        # The code is super ugly and maybe can be improved but idc
        for h in enumerate(list(data.results[-1]["hyperparameters"].values())):
            if list(hp_values.values())[h[0]] != h[1]:
                new_hyperparameters = True
                break

    if new_hyperparameters:
        data.results.append({
            "scores": [score],
            "avg_score": score,
            "hyperparameters": hp_values
        })
    else:
        data.results[-1]["scores"].append(score)
        data.results[-1]["avg_score"] = np.average(data.results[-1]["scores"])