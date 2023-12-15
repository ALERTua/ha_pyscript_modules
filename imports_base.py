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

# if TYPE_CHECKING:
#     from logging import Logger
#     log: Logger
#     from pyscript import State
#     state: State
#     from homeassistant.core import HomeAssistant, State
#     homeassistant: Any
#     hass: HomeAssistant
#     state: State
#     state_active: Callable
#     state_trigger: Callable
#     mqtt_trigger: Callable
#     time_trigger: Callable
#     time_active: Callable
#     event_trigger: Callable
#     task: Any
#     group: Any
#     light: Any
#     switch: Any
#     script: Any
#     sensor: Any
#     cover: Any
#     hassio: Any
#     fan: Any
#     service: Any
#     persistent_notification: Any
#     input_boolean: Any
#     binary_sensor: Any
#     telegram_bot: Any
#     media_player: Any
#     pyscript: Any
#     notify: Any
#     tts: Any
#     xiaomi_aqara: Any
#     ssh_command: Any
#     vacuum: Any
#     input_number: Any
#     input_select: Any
#     climate: Any
#     mqtt: Any
#     task_unique: Any
#     scene: Any
#     number: Any


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


def entity_exists(entity_id):
    return f"hass.states.get(f'{entity_id}') is not None and {entity_id} not in {UNK_S}"
    # return f"hass.states.get('{entity_id}') is not None"


def entity_on(entity_id):
    return f"{entity_id} == 'on'"


def entity_not_on(entity_id):
    return f"{entity_id} != 'on'"


def entity_off(entity_id):
    return f"{entity_id} == 'off'"


def entity_not_off(entity_id):
    return f"{entity_id} != 'off'"
