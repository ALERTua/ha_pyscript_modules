import pendulum
from random import randint, choice
from pprint import pprint, pformat
from pathlib import Path
from functools import lru_cache, partial
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, List, Dict, Collection, Callable, Any
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


# Enable the automation only if all passed conditions are true
def conditional(*conditions, and_=True):
    """
    @conditional(
        "sensor.example1 == 'on'",
        "sensor.example2 == 'off'",
        "sensor.example3 == 'on'",
    )
    """

    def decorator(fn):
        cond = 'all' if and_ else 'any'
        conditions_str = ", ".join(conditions)
        expr = f"{cond}([{conditions_str}])"

        @functools.wraps(fn)
        @state_active(expr)
        def wrapper():
            return fn()
        return wrapper
    return decorator


def _entity_exists(entity_id):
    return f"(hass.states.get(f'{entity_id}') is not None and {entity_id} not in {UNK_S})"
    # return f"hass.states.get('{entity_id}') is not None"


def entity_exists(*entity_ids):
    msg = ''
    for entity_id in entity_ids:
        msg += f"(hass.states.get(f'{entity_id}') is not None and {entity_id} not in {UNK_S}), "

    output = f"all([{msg}])"
    # log.debug(f"entity_exists: {output}")
    return output


def entity_on(entity_id):
    return f"({entity_id} in ('on', 'home'))"


def entity_not_on(entity_id):
    return f"({entity_id} not in ('on', 'home'))"


def entity_off(entity_id):
    return f"({entity_id} in ('off', 'away'))"


def entity_not_off(entity_id):
    return f"({entity_id} not in ('off', 'away'))"
