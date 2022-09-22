# https://github.com/custom-components/pyscript
# https://hacs-pyscript.readthedocs.io/en/stable/
from imports import *


class HA:
    def __init__(self):
        self.timezone = None

    def ha_init(self):
        self.timezone = hass.config.time_zone
