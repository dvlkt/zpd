from random import *
from math import *

learning_rate = 0.5
discount_factor = 0.8
q0 = 1
epsilon = 0.1

q_table = {}

last_action = None
last_state = None

def init(data,load):
    global q_table

    if load != None:
        q_table = load

def update(data):
    global q_table, last_action, last_state

    state = str(data["state"])

    if not state in q_table:
        q_table[state] = [q0 for i in range(data["action_count"]+1)]
    
    # Update previous state/action Q values
    if last_action != None or last_state != None:
        if data["lost"]:
            reward = -1000000
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

    """ if str(data['view']) in q_table:
        sQtable=q_table[str(data["view"])]

        #handles the previous data table
        if data['lost']:
            reward=-1000000
        else:
            reward=1
        if PQtable!=None:
            PQtable[Paction]=PQtable[Paction]-learning_rate*(PQtable[Paction]-(reward+discount_factor*max(SQtable)))
        action_r=random()
        if action_r>epsilon:
            action=q_table[str(data["view"])].index(max(q_table[str(data["view"])]))
            return action-1
        else:
            action=randint(0,len(q_table[str(data["view"])])-1)
            return action-1
        PQtable=sQtable
        Paction=action
    else:
        q_table[str(data["view"])]=[0 for i in range(data["action_count"]+1)]
    return 0 """

def save():
    return q_table

