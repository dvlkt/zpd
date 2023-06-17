import os
from typing import List

import log
import config

current = None # The script for the current algorithm

def get_available_algorithms() -> List[str]:
    results = []

    for a in os.listdir(os.path.join(config.directory, "algorithms")):
        if a[-3:] == ".py" and a != "__init__.py":
            results.append(a[:-3])
    
    return results

def get_save_data() -> str | None:
    if current != None:
        return current.save()
    else:
        return None

def set_current() -> bool:
    global current

    if current != None:
        log.error("Mēģinājums nomainīt algoritmu kamēr tas jau ir iestatīts")
        return
    
    if not config.algorithm in get_available_algorithms():
        log.warn(f"Nezināms algoritms: \"{config.algorithm}\". Tiks izmantots \"{config.DEFAULT_ALGORITHM}\"")

        if config.algorithm == None:
            set_algorithm(config.DEFAULT_ALGORITHM)
        
        return

    current = __import__(f"algorithms.{config.algorithm}", fromlist=["init", "update", "save"])
    
    return False