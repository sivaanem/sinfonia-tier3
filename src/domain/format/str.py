from colorama import Fore, Back


# Format strings
_BOLD = '\033[1m'
_END = '\033[0m'


def white(*tp) -> str:
    """Returns a white-colored string."""
    t = ' '.join(tp)
    return Fore.WHITE + t + Fore.RESET

def cyan(*tp) -> str:
    """Returns a cyan-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTCYAN_EX + t + Fore.RESET

def magenta(*tp) -> str:
    """Returns a magenta-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTMAGENTA_EX + t + Fore.RESET

def cyan_bg(*tp) -> str:
    """Returns a string with cyan background."""
    t = ' '.join(tp)
    return Back.LIGHTCYAN_EX + t + Back.RESET

def red(*tp) -> str:
    """Returns a red-colored string."""
    t = ' '.join(tp)
    return Fore.RED + t + Fore.RESET

def red_bg(*tp) -> str:
    """Returns a string with red background and black foreground."""
    t = ' '.join(tp)
    return Back.RED + Fore.BLACK + t + Fore.RESET + Back.RESET

def green(*tp) -> str:
    """Returns a green-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTGREEN_EX + t + Fore.RESET

def green_bg(*tp) -> str:
    """Returns a string with green background and white foreground."""
    t = ' '.join(tp)
    return Back.LIGHTGREEN_EX + Fore.WHITE + t + Fore.RESET + Back.RESET

def yellow(*tp) -> str:
    """Returns a yellow-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTYELLOW_EX + t + Fore.RESET

def bold(*tp) -> str:
    """Returns a bolded string."""
    t = ' '.join(tp)
    return _BOLD + t + _END
