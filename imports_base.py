import pendulum
from pprint import pprint, pformat
from pathlib import Path
# from cashews import cache
from functools import lru_cache, partial
import homeassistant
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, List, Dict, Collection

if TYPE_CHECKING:
    from logging import Logger
    log: Logger
    from pyscript import State
    state: State
    from homeassistant.core import HomeAssistant, State
    hass: HomeAssistant
    state: State
