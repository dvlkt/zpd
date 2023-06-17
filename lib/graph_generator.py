import matplotlib.pyplot as plt
import numpy as np

import algo_handler
import game_handler
import log

def __gen_1hp_graph():
    log.error("Pašlaik programma vēl neatbalsta grafikus ar 1 hiperparametru!")

def __gen_2hp_graph():
    # Process the data
    hp1_values = []
    hp2_values = []
    score_values = []

    prev_hp = None
    for r in game_handler.data.results:
        curr_hp = list(r["hyperparameters"].values())
        if curr_hp != prev_hp:
            hp1_values.append(curr_hp[0])
            hp2_values.append(curr_hp[1])
            score_values.append([])
        
        score_values[-1].append(r["score"])
        
        prev_hp = curr_hp
    
    avg_scores = []
    for s in score_values:
        avg_scores.append(np.average(s))
    
    log.verbose(f"Grafikā iekļauti {len(avg_scores)} punkti")
    
    # Create the plot
    levels = np.linspace(np.min(avg_scores), np.max(avg_scores), 7)

    fig, ax = plt.subplots()

    ax.plot(hp1_values, hp2_values, "o", markersize=1, color="lightgrey")
    ax.tricontour(hp1_values, hp2_values, avg_scores, levels=levels)

    plt.show()


def generate_graph():
    hp_count = len(algo_handler.hp.hyperparameters)
    
    if hp_count > 0:
        log.log("Ģenerē grafiku...")

    if hp_count == 1:
        log.verbose("Tiks ģenerēts grafiks ar 1 hiperparametru")
        return __gen_1hp_graph()
    elif hp_count == 2:
        log.verbose("Tiks ģenerēts grafiks ar 2 hiperparametriem")
        return __gen_2hp_graph()
    else:
        log.verbose("Netiks ģenerēts grafiks")
        return