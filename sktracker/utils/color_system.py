__all__ = ['color', ]

CODE = {
    'ENDC': 0,  # RESET COLOR
    'BOLD': 1,
    'UNDERLINE': 4,
    'BLINK': 5,
    'INVERT': 7,
    'CONCEALD': 8,
    'STRIKE': 9,
    'GREY30': 90,
    'GREY40': 2,
    'GREY65': 37,
    'GREY70': 97,
    'GREY20_BG': 40,
    'GREY33_BG': 100,
    'GREY80_BG': 47,
    'GREY93_BG': 107,
    'DARK_RED': 31,
    'RED': 91,
    'RED_BG': 41,
    'LIGHT_RED_BG': 101,
    'DARK_YELLOW': 33,
    'YELLOW': 93,
    'YELLOW_BG': 43,
    'LIGHT_YELLOW_BG': 103,
    'DARK_BLUE': 34,
    'BLUE': 94,
    'BLUE_BG': 44,
    'LIGHT_BLUE_BG': 104,
    'DARK_MAGENTA': 35,
    'PURPLE': 95,
    'MAGENTA_BG': 45,
    'LIGHT_PURPLE_BG': 105,
    'DARK_CYAN': 36,
    'AUQA': 96,
    'CYAN_BG': 46,
    'LIGHT_AUQA_BG': 106,
    'DARK_GREEN': 32,
    'GREEN': 92,
    'GREEN_BG': 42,
    'LIGHT_GREEN_BG': 102,
    'BLACK': 30,
}

def _termcode(num):
    return '\033[%sm' % num


def color(astr, color='ENDC'):
    """Colorized string variable.

    Parameters
    ----------
    astr: string
        String to colorize.
    color: string
        Which color to use (ENDC means "reset color"):

        'ENDC', 'BOLD', 'UNDERLINE', 'BLINK', 'INVERT', 'CONCEALD', 'STRIKE', 'GREY30',
        'GREY40', 'GREY65', 'GREY70', 'GREY20_BG', 'GREY33_BG', 'GREY80_BG',
        'GREY93_BG', 'DARK_RED', 'RED', 'RED_BG', 'LIGHT_RED_BG', 'DARK_YELLOW',
        'YELLOW', 'YELLOW_BG', 'LIGHT_YELLOW_BG', 'DARK_BLUE', 'BLUE', 'BLUE_BG',
        'LIGHT_BLUE_BG', 'DARK_MAGENTA', 'PURPLE', 'MAGENTA_BG', 'LIGHT_PURPLE_BG',
        'DARK_CYAN', 'AUQA', 'CYAN_BG', 'LIGHT_AUQA_BG', 'DARK_GREEN', 'GREEN',
        'GREEN_BG', 'LIGHT_GREEN_BG', 'BLACK'

    Returns
    -------
    String with colored terminal code.

    Examples
    --------
    >>> from sktracker.utils import color
    >>> print(color("I am a RED string", "RED"))
    I am a RED string
    >>>  # Displayed in red in a terminal

    """
    return _termcode(CODE[color]) + astr + _termcode(CODE['ENDC'])
