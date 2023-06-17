from random import *
from math import *

learning_rate = 0.2
discount_factor = 0.9
q0 = 10
epsilon = 0.05

q_table = {}

last_action = None
last_state = None

def init(data, load):
    global q_table

    if load != None:
        q_table = load
    
    return [("Mācīšanās ātrums", 0, 1), ("Atlaides faktors", 0, 1)]

def update(data, hyperparameters):
    global learning_rate, discount_factor, q_table, last_action, last_state

    if hyperparameters != None:
        q_table = {}
        last_action = None
        last_state = None

        learning_rate = hyperparameters[0]
        discount_factor = hyperparameters[1]

    state = str(data["state"])

    if not state in q_table:
        q_table[state] = [q0 for i in range(data["action_count"]+1)]
    
    # Update previous state/action Q values
    if last_action != None or last_state != None:
        if data["lost"]:
            reward = -10
        else:
            reward = 1
        
        q_table[last_state][last_action] = q_table[last_state][last_action] - learning_rate * (q_table[last_state][last_action] - (reward + discount_factor * max(q_table[state])))
    
    # Execute an action
    n = random()
    if n >= epsilon:
        action = q_table[state].index(max(q_table[state]))
    else:
        action = randint(0, data["action_count"]-1)
    
    last_action = action
    last_state = state

    return action - 1

def save():
    return q_table

