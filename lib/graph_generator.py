import matplotlib.pyplot as plt
import numpy as np

import algorithm
import server.data
import log

def generate_graph(is_silent=False):
    if not is_silent:
        log.log("Ģenerē grafiku...")
    
    plt.close() # Close all of the previous plots to save memory

    learning_rate_values = []
    discount_factor_values = []
    avg_scores = []
    
    for r in server.data.results:
        learning_rate_values.append(r["hyperparameters"][0])
        discount_factor_values.append(r["hyperparameters"][1])
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
    ax.plot(learning_rate_values, discount_factor_values, "o", markersize=1, color="grey")
    ax.tricontour(learning_rate_values, discount_factor_values, avg_scores, levels=levels)

    return fig