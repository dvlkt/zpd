import os
from typing import List

import log
import config

current = __import__(f"algorithms.algorithm", fromlist=["init", "update", "save"])

def save() -> str | None:
    return current.save()