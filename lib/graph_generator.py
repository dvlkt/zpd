import matplotlib.pyplot as plt
import numpy as np

import algo_handler
import game_handler
import log

def __gen_1hp_graph(is_silent):
    if not is_silent:
        log.error("Pašlaik programma vēl neatbalsta grafikus ar 1 hiperparametru!")

def __gen_2hp_graph(is_silent):
    # Process the data
    hp1_values = []
    hp2_values = []
    avg_scores = []

    for r in game_handler.data.results:
        curr_hp = list(r["hyperparameters"].values())
        hp1_values.append(curr_hp[0])
        hp2_values.append(curr_hp[1])
        avg_scores.append(r["avg_score"])
    
    if len(avg_scores) < 3:
        if not is_silent:
            log.warn("Netiks izveidots grafiks, jo tam ir nepieciešami vismaz 3 datu punkti")
        return
    
    if not is_silent:
        log.verbose(f"Grafikā iekļauti {len(avg_scores)} punkti")
    
    # Create the plot
    levels = np.linspace(np.min(avg_scores), np.max(avg_scores), 7)

    fig, ax = plt.subplots()

    ax.plot(hp1_values, hp2_values, "o", markersize=1, color="grey")
    ax.tricontour(hp1_values, hp2_values, avg_scores, levels=levels)

    return fig

def __gen_3hp_graph(is_silent):
    if not is_silent:
        log.error("Pašlaik programma vēl neatbalsta grafikus ar 3 hiperparametriem!")


def generate_graph(is_silent=False):
    if algo_handler.hp.hyperparameters == None:
        log.verbose("Netiks ģenerēts grafiks")
        return

    hp_count = len(algo_handler.hp.hyperparameters)
    
    if hp_count > 0:
        if not is_silent:
            log.log("Ģenerē grafiku...")

    if hp_count == 1:
        if not is_silent:
            log.verbose("Tiks ģenerēts grafiks ar 1 hiperparametru")
        return __gen_1hp_graph(is_silent)
    elif hp_count == 2:
        if not is_silent:
            log.verbose("Tiks ģenerēts grafiks ar 2 hiperparametriem")
        return __gen_2hp_graph(is_silent)
    elif hp_count == 3:
        if not is_silent:
            log.verbose("Tiks ģenerēts grafiks ar 3 hiperparametriem")
        return __gen_3hp_graph(is_silent)
    else:
        if not is_silent:
            log.verbose("Netiks ģenerēts grafiks")
        return