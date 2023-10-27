from random import *
from math import *

learning_rate = None
discount_factor = None

q0 = 10
epsilon = 0.05
good_reward = 1
bad_reward = -10

q_table = {}

last_action = None
last_state = None

def update(data) -> int:
    global learning_rate, discount_factor, q_table, last_action, last_state

    state = str(data["state"])

    if not state in q_table:
        q_table[state] = [q0 for i in range(data["action_count"]+1)]
    
    # Update previous state/action Q values
    if last_action != None or last_state != None:
        if data["lost"]:
            reward = bad_reward
        else:
            reward = good_reward
        
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

def reset() -> None:
    global q_table, last_action, last_state

    q_table = {}
    last_action = None
    last_state = None