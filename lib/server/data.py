import algorithm
import numpy as np

action_count = None

curr_score = 0
curr_state = []
reward = 0
has_lost = False

played_episodes = 0

results = []
def add_result(score: int) -> None:
    global results

    new_hyperparameters: bool = False
    if len(results) == 0:
        new_hyperparameters = True
    else:
        new_hyperparameters = results[-1]["hyperparameters"] != [algorithm.learning_rate, algorithm.discount_factor]

    if new_hyperparameters:
        results.append({
            "scores": [score],
            "avg_score": score,
            "hyperparameters": [algorithm.learning_rate, algorithm.discount_factor]
        })
    else:
        results[-1]["scores"].append(score)
        results[-1]["avg_score"] = np.average(results[-1]["scores"])