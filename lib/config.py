import os

directory: str = os.path.join(os.path.dirname(os.path.realpath(__file__)))

DEFAULT_PORT = 1789
port: int = None

DEFAULT_ALGORITHM = "random"
algorithm: str = None

episodes_per_hyperparameter: int = 100

DEFAULT_HP_ADJUSTMENT_STRATEGY = "default"
VALID_HP_ADJUSTMENT_STRATEGIES = ["default", "random", "grid"]
hp_adjustment_strategy: str = None

create_graphs: bool = True

is_verbose: bool = False

input_file_name: str | None = None

output_file_name: str | None = None

autosave_interval: int | None = None