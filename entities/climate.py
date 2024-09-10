# https://github.com/custom-components/pyscript
from imports_base import *
from entities.switch import Switch


class Climate(Switch):
    """
    {
        'entity_id': 'climate.ac_office',
        'state': 'fan_only',
        'attributes': {
            'hvac_modes': [
                "<HVACMode.FAN_ONLY: 'fan_only'>",
                "<HVACMode.DRY: 'dry'>",
                "<HVACMode.COOL: 'cool'>",
                "<HVACMode.HEAT: 'heat'>",
                "<HVACMode.HEAT_COOL: 'heat_cool'>",
                "<HVACMode.OFF: 'off'>"
            ],
            'min_temp': 7,
            'max_temp': 35,
            'target_temp_step': 1,
            'fan_modes': [
                'Auto', 'Silence', '1', '2', '3', '4', '5'
            ],
            'preset_modes': ['none', 'away', 'eco', 'boost'],
            'swing_modes': ['Off', 'Vertical', 'Horizontal', '3D'],
            'current_temperature': 24.0,
            'temperature': None,
            'fan_mode': '2',
            'preset_mode': 'none',
            'swing_mode': 'Vertical',
            'friendly_name': 'OfficeAC',
            'supported_features': "<ClimateEntityFeature.TARGET_TEMPERATURE|FAN_MODE|PRESET_MODE|SWING_MODE|TURN_OFF|TURN_ON: 441>"
        },
        'last_changed': '2024-05-02T12:00:12.825057+00:00', 'last_reported': '2024-05-02T12:05:20.180818+00:00',
        'last_updated': '2024-05-02T12:05:20.180818+00:00',
        'context': {'id': '01HWWK3Q5M86HYM5SYD8A0Y2MN', 'parent_id': None, 'user_id': None}
    }
    """
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def hvac_mode(self):
        return self.state()

    def preset_mode(self):
        return self.state('preset_mode')

    def swing_mode(self):
        return self.state('swing_mode')

    def current_temperature(self):
        return self.state('current_temperature')

    def fan_mode(self):
        output = self.state('fan_mode')
        return output

    def set_hvac_mode(self, hvac_mode, *args, **kwargs):
        # log.debug(f"set_hvac_mode for {self} to {hvac_mode}")
        if self.ha_state is None:
            return

        return climate.set_hvac_mode(entity_id=self.entity_id, hvac_mode=hvac_mode, *args, **kwargs)

    def set_preset_mode(self, preset_mode, *args, **kwargs):
        # log.debug(f"set_preset_mode for {self.as_str()} to {preset_mode}")
        if self.ha_state is None:
            return

        return climate.set_preset_mode(entity_id=self.entity_id, preset_mode=preset_mode, *args, **kwargs)

    def set_temperature(self, hvac_mode=None, temperature=None, target_temp_high=None, target_temp_low=None, *args, **kwargs):
        if self.ha_state is None:
            return

        # hvac_mode = hvac_mode or self.state()  # AC needs this, valves don't
        # log.debug(f"set_temperature for {self.as_str()} to hvac_mode: {hvac_mode} temperature: {temperature} target_temp_high: {target_temp_high} target_temp_low: {target_temp_low}")
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
            action: climate.set_fan_mode
            data:
            fan_mode: Auto
            target:
            entity_id: climate.ac_office
        """
        if self.ha_state is None:
            return

        # log.debug(f"set_fan_mode for {self.as_str()} to {fan_mode}")
        return climate.set_fan_mode(entity_id=self.entity_id, fan_mode=fan_mode, *args, **kwargs)
