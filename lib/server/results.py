import numpy as np

import server.data as data
import algorithm

def add(score: int) -> None:
    new_hyperparameters: bool = False
    if len(data.results) == 0:
        new_hyperparameters = True
    else:
        new_hyperparameters = data.results[-1]["hyperparameters"] != [algorithm.learning_rate, algorithm.discount_factor]

    if new_hyperparameters:
        data.results.append({
            "scores": [score],
            "avg_score": score,
            "hyperparameters": [algorithm.learning_rate, algorithm.discount_factor]
        })
    else:
        data.results[-1]["scores"].append(score)
        data.results[-1]["avg_score"] = np.average(data.results[-1]["scores"])