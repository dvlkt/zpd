import datetime
from colorama import Fore, Style

import config

file_log = ""

def __get_timestamp() -> str:
    now = datetime.datetime.now()
    return now.time()

def __print_to_file(msg: str):
    global file_log
    file_log += f"[{__get_timestamp()}] {msg}\n"

def __print_to_terminal(msg: str) -> None:
    print(f"{Style.DIM}[{__get_timestamp()}]{Style.RESET_ALL} {msg}{Style.RESET_ALL}")

def verbose(msg: str) -> None:
    __print_to_file(msg)
    if config.is_verbose:
        __print_to_terminal(msg)

def log(msg: str) -> None:
    __print_to_file(msg)
    __print_to_terminal(msg)

def warn(msg: str) -> None:
    __print_to_file(f"BRĪDINĀJUMS: {msg}")
    __print_to_terminal(f"{Fore.YELLOW}BRĪDINĀJUMS: {msg}")

def error(msg: str) -> None:
    __print_to_file(f"KĻŪDA: {msg}")
    __print_to_terminal(f"{Fore.RED}KĻŪDA: {msg}")