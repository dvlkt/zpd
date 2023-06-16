import datetime
from colorama import Fore, Style

__file_log = ""

def __get_timestamp() -> str:
    now = datetime.datetime.now()
    return now.time()

def __add_to_file(msg: str):
    global __file_log
    __file_log += f"[{__get_timestamp()}] {msg}"

def __add_to_terminal(msg: str) -> None:
    print(f"{Style.DIM}[{__get_timestamp()}]{Style.RESET_ALL} {msg}{Style.RESET_ALL}")


def verbose(msg: str) -> None:
    __add_to_file(msg)
    if config.is_verbose:
        __add_to_terminal(msg)

def log(msg: str) -> None:
    __add_to_file(msg)
    __add_to_terminal(msg)

def warn(msg: str) -> None:
    __add_to_file(f"BRĪDINĀJUMS: {msg}")
    __add_to_terminal(f"{Fore.YELLOW}BRĪDINĀJUMS: {msg}")

def error(msg: str) -> None:
    __add_to_file(f"KĻŪDA: {msg}")
    __add_to_terminal(f"{Fore.RED}KĻŪDA: {msg}")


def save_log(filename: str) -> None:
    return