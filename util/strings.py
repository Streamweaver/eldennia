from enum import Enum

class ANSI(Enum):
    # Mostly taken from the Evennia util class, put into enum for eash of use.
    BEEP = "\07"
    ESC = "\033"
    NORMAL = "\033[0m"

    UNDERLINE = "\033[4m"
    HILITE = "\033[1m"
    UNHILITE = "\033[22m"
    BLINK = "\033[5m"
    INVERSE = "\033[7m"
    INV_HILITE = "\033[1;7m"
    INV_BLINK = "\033[7;5m"
    BLINK_HILITE = "\033[1;5m"
    INV_BLINK_HILITE = "\033[1;5;7m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_READ = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Formatting Characters
    RETURN = "\r\n"
    TAB = "\t"

def _wrap(color, msg):
    return "".join([color, msg, ANSI.NORMAL])

def magenta(msg):
    return _wrap(ANSI.MAGENTA, msg)
def blue(msg):
    return _wrap(ANSI.BLUE, msg)
def yellow(msg):
    return _wrap(ANSI.YELLOW, msg)
def red(msg):
    return _wrap(ANSI.RED, msg)
def green(msg):
    return _wrap(ANSI.GREEN, msg)
def cyan(msg):
    _wrap(ANSI.CYAN, msg)
def white(msg):
    _wrap(ANSI.WHITE, msg)
def hilite(msg):
    return _wrap(ANSI.HILITE, msg)