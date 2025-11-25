# https://github.com/custom-components/pyscript
from homeassistant.config_entries import ConfigEntry, ConfigEntryDisabler
from imports_base import *


class Config_Entry:
    # noinspection PyMissingConstructor
    def __init__(self, config_entry_id: str):
        self.config_entry_id: str = config_entry_id

    def hass_config_entry(self)-> ConfigEntry:
        config_entry_id = self.config_entry_id
        return hass.config_entries.async_get_entry(config_entry_id)

    def disabled(self):
        config_entry_id = self.config_entry_id
        return template.config_entry_attr(hass, config_entry_id, attr_name='disabled_by') is not None

    def disable(self):
        config_entry_id = self.config_entry_id
        hass.config_entries.async_set_disabled_by(entry_id=config_entry_id, disabled_by=ConfigEntryDisabler.USER)

    def enable(self):
        config_entry_id = self.config_entry_id
        hass.config_entries.async_set_disabled_by(entry_id=config_entry_id, disabled_by=None)

    def reload(self):
        config_entry_id = self.config_entry_id
        hass.config_entries.async_reload(entry_id=config_entry_id)
