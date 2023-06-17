import random

import config
import algo_handler.hp as hp

def __random_adjust() -> None:
    for h in hp.hyperparameters:
        h["value"] = random.uniform(h["min"], h["max"])


def __bayesian_adjust() -> None:
    __random_adjust()


def adjust() -> None:
    if config.hp_adjustment_strategy == "bayesian":
        __bayesian_adjust()
    elif config.hp_adjustment_strategy == "random":
        __random_adjust()