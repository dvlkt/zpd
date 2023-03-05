import os

current_name = ""
current = None
is_initialized = False # True if the init() function has been called for the current algorithm

def set_algorithm(value):
    global current_name, current, is_current_init
    current_name = value
    current = __import__(f"algorithms.{current_name}", fromlist=["init", "update", "save"])
    is_initialized = False
set_algorithm("random")

def set_initialized():
    global is_initialized
    is_initialized = True

available = []
for a in os.listdir("algorithms"):
    if a[-3:] == ".py" and a != "__init__.py":
        available.append(a[:-3])