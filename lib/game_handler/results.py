import game_handler.data as data

def add(score) -> None:
    data.results.append({
        "score": score,
        "hyperparameters": {}
    })