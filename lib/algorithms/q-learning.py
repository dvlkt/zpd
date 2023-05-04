from random import *
from math import *
alpha=0.5
gamma=0.8
epsilon=1
Q_table={}
PQtable=None
def init(data,load):
    global Q_table,acount
    Q_table={}
    acount=data["action_count"]
def update(data):
    global Q_table,PQtable,Paction
    if str(data['view']) in Q_table:
        sQtable=Q_table[str(data["view"])]
        #handles the previous data table
        if data['lost']:
            reward=-1000000
        else:
            reward=1
        if PQtable!=None:
            PQtable[Paction]=PQtable[Paction]-alpha*(PQtable[Paction]-(reward+gamma*max(SQtable)))
        action_r=random()
        if action_r>epsilon:
            action=Q_table[str(data["view"])].index(max(Q_table[str(data["view"])]))
            return action-1
        else:
            action=randint(0,len(Q_table[str(data["view"])])-1)
            return action-1
        PQtable=sQtable
        Paction=action
    else:
        Q_table[str(data["view"])]=[0 for i in range(data["action_count"]+1)]
    return 0
def save():
    return Q_table
