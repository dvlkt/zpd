from random import random, randint

learning_rate = None
discount_factor = None

q0 = 10
epsilon = 0.05

q_table = {}

last_action = None
last_state = None

def update(action_count, state, reward) -> int:
    global learning_rate, discount_factor, q_table, last_action, last_state
    
    if not state in q_table:
        q_table[state] = [q0 for i in range(action_count+1)]
        
    # Update previous state/action Q values
    if last_action != None or last_state != None:        
        q_table[last_state][last_action] = q_table[last_state][last_action] - learning_rate * (q_table[last_state][last_action] - (reward + discount_factor * max(q_table[state])))
    
    # Execute an action
    n = random()
    if n >= epsilon:
        action = q_table[state].index(max(q_table[state]))
    else:
        action = randint(0, action_count)
    
    last_action = action
    last_state = state

    return action - 1

def reset() -> None:
    global q_table, last_action, last_state

    q_table = {}
    last_action = None
    last_state = None