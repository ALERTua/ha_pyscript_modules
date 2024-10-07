# https://github.com/custom-components/pyscript
from homeassistant.util.color import brightness_to_value
from entities.switch import Switch


class Light(Switch):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def brightness_percent(self):
        brightness_value = self.state('brightness', 0)
        brightness_value = brightness_value or 0
        return int(round(brightness_to_value((1, 100), int(brightness_value)), 0))
