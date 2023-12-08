# https://github.com/custom-components/pyscript
from imports_base import *
from entities.switch import Switch


class Climate(Switch):
    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, priority_mode=False, allow_unknown=False):
        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.entity_init()

    def set_hvac_mode(self, hvac_mode, *args, **kwargs):
        log.debug(f"set_hvac_mode for {self} to {hvac_mode}")
        if self.entity is None:
            return

        return climate.set_hvac_mode(entity_id=self.entity_id, hvac_mode=hvac_mode, *args, **kwargs)

    def set_preset_mode(self, preset_mode, *args, **kwargs):
        log.debug(f"set_preset_mode for {self.as_str()} to {preset_mode}")
        if self.entity is None:
            return

        return climate.set_preset_mode(entity_id=self.entity_id, preset_mode=preset_mode, *args, **kwargs)

    def set_temperature(self, hvac_mode=None, temperature=None, target_temp_high=None, target_temp_low=None, *args, **kwargs):
        if self.entity is None:
            return

        # hvac_mode = hvac_mode or self.state()  # AC needs this, valves don't
        log.debug(f"set_temperature for {self.as_str()} to hvac_mode: {hvac_mode} temperature: {temperature} target_temp_high: {target_temp_high} target_temp_low: {target_temp_low}")
        return climate.set_temperature(entity_id=self.entity_id, hvac_mode=hvac_mode, temperature=temperature, target_temp_high=target_temp_high, target_temp_low=target_temp_low, *args, **kwargs)

    def set_fan_mode(self, fan_mode, *args, **kwargs):
        """
            service: climate.set_fan_mode
            data:
            fan_mode: Auto
            target:
            entity_id: climate.ac_office
        """
        if self.entity is None:
            return

        log.debug(f"set_fan_mode for {self.as_str()} to {fan_mode}")
        return climate.set_fan_mode(entity_id=self.entity_id, fan_mode=fan_mode, *args, **kwargs)
