import pendulum
from random import randint, choice
from pprint import pprint, pformat
from pathlib import Path
from functools import lru_cache, partial
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, List, Dict, Collection, Callable, Any
from copy import copy
import functools


if TYPE_CHECKING:
    from logging import Logger
    log: Logger
    from pyscript import State
    state: State
    from homeassistant.core import HomeAssistant, State
    hass: HomeAssistant
    state: State
    state_active: Callable
    state_trigger: Callable
    mqtt_trigger: Callable
    time_trigger: Callable
    time_active: Callable
    event_trigger: Callable
    task: Any
    group: Any
    light: Any
    switch: Any
    script: Any
    sensor: Any
    cover: Any
    hassio: Any
    fan: Any
    service: Any
    persistent_notification: Any
    input_boolean: Any
    binary_sensor: Any
    telegram_bot: Any
    media_player: Any
    pyscript: Any
    notify: Any
    tts: Any
    xiaomi_aqara: Any
    ssh_command: Any
