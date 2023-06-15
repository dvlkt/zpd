import random

def init(data, load):
    return []

def update(data, hyperparameters):
    return max(random.randint(-20, data["action_count"] - 1), -1)

def save():
    return {}