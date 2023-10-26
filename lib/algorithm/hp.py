from typing import List, Dict
import random

hyperparameters = None

def init(values) -> None:
    global hyperparameters
    
    hyperparameters = []
    for v in values:
        hyperparameters.append({
            "name": v[0],
            "value": None,
            "min": v[1],
            "max": v[2]
        })
    
    if len(hyperparameters) > 2: # Cap the hyperparameter count at 2
        hyperparameters = hyperparameters[:1]

def get_values() -> List[float]:
    if len(hyperparameters) == 0:
        return []

    results = []
    for h in hyperparameters:
        results.append(h["value"])
    return results

def get_named_values() -> Dict[str, float]:
    if len(hyperparameters) == 0:
        return {}

    results = {}
    for h in hyperparameters:
        results[h["name"]] = h["value"]
    return results