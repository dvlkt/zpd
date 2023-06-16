import game_handler.data as data
import algo_handler.hp

def add(score) -> None:
    data.results.append({
        "score": score,
        "hyperparameters": algo_handler.hp.get_named_values()
    })