import os
import data, saving

current_name = ""
current = None

is_initialized = False # True if the init() function has been called for the current algorithm
def set_initialized():
    global is_initialized
    is_initialized = True

available = []
for a in os.listdir(os.path.join(data.directory, "algorithms")):
    if a[-3:] == ".py" and a != "__init__.py":
        available.append(a[:-3])

def set_algorithm(value):
    global current_name, current, is_current_init, available

    if not value in available:
        print(f"⚠️  Nezināms algoritms \"{value}\". Tiks izmantots \"{current_name}\".")
        return

    current_name = value
    current = __import__(f"algorithms.{current_name}", fromlist=["init", "update", "save"])
    is_initialized = False
    saving.statistics = None
set_algorithm("random")

def get_save_data():
    if current != None:
        return current.save()
    else:
        return None