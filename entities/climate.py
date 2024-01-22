# https://github.com/custom-components/pyscript
from entities.switch import Switch


class Climate(Switch):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def set_hvac_mode(self, hvac_mode, *args, **kwargs):
        log.debug(f"set_hvac_mode for {self} to {hvac_mode}")
        if self.ha_state is None:
            return

        return climate.set_hvac_mode(entity_id=self.entity_id, hvac_mode=hvac_mode, *args, **kwargs)

    def set_preset_mode(self, preset_mode, *args, **kwargs):
        log.debug(f"set_preset_mode for {self.as_str()} to {preset_mode}")
        if self.ha_state is None:
            return

        return climate.set_preset_mode(entity_id=self.entity_id, preset_mode=preset_mode, *args, **kwargs)

    def set_temperature(self, hvac_mode=None, temperature=None, target_temp_high=None, target_temp_low=None, *args, **kwargs):
        if self.ha_state is None:
            return

        # hvac_mode = hvac_mode or self.state()  # AC needs this, valves don't
        log.debug(f"set_temperature for {self.as_str()} to hvac_mode: {hvac_mode} temperature: {temperature} target_temp_high: {target_temp_high} target_temp_low: {target_temp_low}")
        kw = dict(entity_id=self.entity_id)
        if hvac_mode is not None:
            kw.update(hvac_mode=hvac_mode)
        if temperature is not None:
            kw.update(temperature=temperature)
        if target_temp_high is not None:
            kw.update(target_temp_high=target_temp_high)
        if target_temp_low is not None:
            kw.update(target_temp_low=target_temp_low)
        return climate.set_temperature(*args, **kw, **kwargs)

    def set_fan_mode(self, fan_mode, *args, **kwargs):
        """
            service: climate.set_fan_mode
            data:
            fan_mode: Auto
            target:
            entity_id: climate.ac_office
        """
        if self.ha_state is None:
            return

        log.debug(f"set_fan_mode for {self.as_str()} to {fan_mode}")
        return climate.set_fan_mode(entity_id=self.entity_id, fan_mode=fan_mode, *args, **kwargs)
