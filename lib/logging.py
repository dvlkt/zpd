import datetime
from colorama import Fore, Style

def __get_timestamp() -> str:
    now = datetime.datetime.now()
    return now.time()

def verbose(message: str) -> None:
    print(f"[{__get_timestamp()}] {message}{Style.RESET_ALL}")

def log(message: str) -> None:
    print(f"[{__get_timestamp()}] {message}{Style.RESET_ALL}")

def warn(message: str) -> None:
    print(f"[{__get_timestamp()}] {Fore.YELLOW}BRĪDINĀJUMS: {message}{Style.RESET_ALL}")

def error(message: str) -> None:
    print(f"[{__get_timestamp()}] {Fore.RED}KĻŪDA: {message}{Style.RESET_ALL}")