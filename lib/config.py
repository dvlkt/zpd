import os

directory: str = os.path.join(os.path.dirname(os.path.realpath(__file__)))

port: int = 1789

DEFAULT_ALGORITHM = "random"
algorithm: str = None

episodes_per_hyperparameter: int = 100

create_graphs: bool = True

is_verbose: bool = False

input_file_name: str | None = None

output_file_name: str | None = None