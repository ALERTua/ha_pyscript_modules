# https://github.com/custom-components/pyscript
from imports_base import *
from entities.switch import Switch


def position_normalize(value):
    value = max(value, 0)
    value = min(value, 100)
    return value


class Window(Switch):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id, reverse=False):
        self.entity_id = entity_id
        self.init()
        self.reverse = reverse

    def position(self):
        dct = self.attrs()
        output = dct.get('current_position', dct.get('position'))
        if output is not None and self.reverse:
            output = 100 - int(output)
        return output

    def position_set(self, value):
        log.debug(f"Setting {self.ha_state} {self.friendly_name()} position to {value}")
        value = position_normalize(value)
        if self.reverse:
            value = 100 - int(value)
        # noinspection PyUnresolvedReferences
        return cover.set_cover_position(entity_id=self.entity_id, position=value)

    def position_add(self, value):
        new_value = position_normalize(self.position() + value)
        return self.position_set(new_value)

    def position_subtract(self, value):
        new_value = position_normalize(self.position() - value)
        return self.position_set(new_value)

    def stop(self):
        return cover.stop_cover(entity_id=self.entity_id)

    def open(self):
        return cover.open_cover(entity_id=self.entity_id)

    def close(self):
        return cover.close_cover(entity_id=self.entity_id)


class Cover(Window):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id, reverse=False):
        self.entity_id = entity_id
        self.reverse = reverse
        self.init()
