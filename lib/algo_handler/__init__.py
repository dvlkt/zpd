import os
from typing import List

import log
import config

current = __import__(f"algorithms.algorithm", fromlist=["init", "update", "save"])

def get_save_data() -> str | None:
    if current != None:
        return current.save()
    else:
        return None