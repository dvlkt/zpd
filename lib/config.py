import os

directory: str = os.path.join(os.path.dirname(os.path.realpath(__file__)))

DEFAULT_PORT = 1789
port: int = None

episodes_per_hyperparameter: int = 100

create_graphs: bool = True

is_verbose: bool = False

input_file_name: str | None = None

output_file_name: str | None = None

autosave_interval: int | None = None