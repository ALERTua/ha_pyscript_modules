# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
import homeassistant.helpers.template as template


class Area:
    def __init__(self, area_name):
        self.name = area_name

    def area_id(self):
        return template.area_id(hass, self.name)

    def entity_ids(self):
        return template.area_entities(hass, self.name)

    def devices(self):
        return template.area_devices(hass, self.name)

