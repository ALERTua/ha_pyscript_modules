import pendulum
from random import randint, choice
from pprint import pprint, pformat
from pathlib import Path
from functools import lru_cache, partial
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, List, Dict, Collection, Callable, Any, Literal, Optional
from copy import copy
import functools
from constants import *
from pyscript_mock import *


UNK_O = ('unavailable', 'unknown', 'null', None, 'none', 'None')
UNK_S = str(UNK_O)

UNK_O_OFF = (*UNK_O, 'off')
UNK_S_OFF = str(UNK_O_OFF)

MEDIA_PATH_BASE = Path('/config/www/media')
EXTERNAL_MEDIA_BASE = '/local/media/'


def conditional(*conditions, and_=True, debug=False):
    """
    @conditional(
        "sensor.example1 == 'on'",
        "sensor.example2 == 'off'",
        "sensor.example3 == 'on'",
    )
    """

    def decorator(fn):
        joint = 'and' if and_ else 'or'
        expr = ''
        for condition in conditions:
            if expr:
                expr += f" {joint} "

            expr += f"{condition}"

        if debug:
            log.debug(f"conditional: {expr}")
        expr = expr.strip()

        @functools.wraps(fn)
        @state_active(expr)
        def wrapper():
            return fn()
        return wrapper
    return decorator


def float_(obj):
    try:
        return float(obj)
    except:
        return -666


def int_(obj):
    try:
        return int(obj)
    except:
        return 666
