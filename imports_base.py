# noinspection PyUnusedImports
from random import randint, choice
# noinspection PyUnusedImports
from pprint import pprint, pformat
from pathlib import Path
# noinspection PyUnusedImports
from functools import lru_cache, partial
# noinspection PyUnusedImports
from datetime import datetime, timedelta, date
# noinspection PyUnusedImports
from typing import TYPE_CHECKING, Iterable, List, Dict, Collection, Callable, Any, Literal, Optional
# noinspection PyUnusedImports
from copy import copy
# noinspection PyUnusedImports
from homeassistant.util import dt as dt_util
# noinspection PyUnusedImports
from homeassistant.const import EVENT_CALL_SERVICE

# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
# noinspection PyUnusedImports
import homeassistant.helpers.template as template

# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/entity.py
# noinspection PyUnusedImports
import homeassistant.helpers.entity as entity_helper

import functools
# noinspection PyUnusedImports
from constants import *
# noinspection PyUnusedImports
from stubs.pyscript_builtins import *
# noinspection PyUnusedImports
from stubs.pyscript_generated import *

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

    if not conditions:

        def decorator(fn):
            @functools.wraps(fn)
            def wrapper():
                return fn()

            return wrapper

        return decorator

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


def float_(obj, default=None):
    try:
        return float(obj)
    except:
        if default is not None:
            return default
        return -666.0


def int_(obj, default=None):
    try:
        return int(float(obj))
    except:
        if default is not None:
            return default
        return -666
