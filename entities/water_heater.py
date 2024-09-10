# https://github.com/custom-components/pyscript
from imports_base import *
from entities.switch import Switch


class WaterHeater(Switch):
    """
    {
    'entity_id': 'water_heater.boiler',
    'state': 'eco',
    'attributes': {
        'min_temp': 50.0,
        'max_temp': 65.0,
        'operation_list': [
            "'<OverkizCommandParam.PERFORMANCE': 'performance'>",
            "<OverkizCommandParam.ECO: 'eco'>",
            "<OverkizCommandParam.MANUAL: 'manual'>"
        ],
        'current_temperature': 60.2,
        'temperature': 65.0,
        'target_temp_high': None,
        'target_temp_low': None,
        'operation_mode': 'eco',
        'away_mode': 'off',
        'friendly_name': 'Boiler',
        'supported_features': "<WaterHeaterEntityFeature.TARGET_TEMPERATURE|OPERATION_MODE|AWAY_MODE|ON_OFF: 15>"
    },
    'last_changed': '2024-07-14T09:50:28.108618+00:00',
    'last_reported': '2024-07-15T12:38:44.377658+00:00',
    'last_updated': '2024-07-15T10:03:04.388018+00:00',
    'context': {'id': '01J2TXH1A482NZV30Z5KHTGFMQ', 'parent_id': None, 'user_id': None}
    }
    """
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def operation_mode(self):
        return self.state()

    def current_temperature(self):
        return self.state('current_temperature')

    def target_temperature(self):
        return self.state('temperature')

    def away_mode(self):
        return self.state('away_mode')

    def away_mode_on(self):
        return self.state('away_mode') == 'on'

    def set_away_mode(self, away_mode):
        log.debug(f"set_away_mode for {self.as_str()} to {away_mode}")
        if self.ha_state is None:
            return

        return water_heater.set_away_mode(entity_id=self.entity_id, away_mode=away_mode)

    def set_operation_mode(self, operation_mode):
        log.debug(f"set_operation_mode for {self.as_str()} to {operation_mode}")
        if self.ha_state is None:
            return

        return water_heater.set_operation_mode(entity_id=self.entity_id, operation_mode=operation_mode)

    def set_temperature(self, operation_mode=None, temperature=None):
        if self.ha_state is None:
            return

        # log.debug(f"set_temperature for {self.as_str()} to operation_mode: {operation_mode} temperature: {temperature}")
        # hvac_mode = hvac_mode or self.state()  # AC needs this, valves don't
        kw = dict(entity_id=self.entity_id)
        if operation_mode is not None:
            kw.update(operation_mode=operation_mode)
        if temperature is not None:
            kw.update(temperature=temperature)
        return water_heater.set_temperature(**kw)
