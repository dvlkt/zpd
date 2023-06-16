import os

directory: str = os.path.join(os.path.dirname(os.path.realpath(__file__)))

port: int = 1789

episodes_per_hyperparameter: int = 100

is_verbose: bool = False

input_file_name: str | None = None

output_file_name: str | None = None