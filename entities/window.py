# https://github.com/custom-components/pyscript
from imports_base import *
from entities.switch import Switch


def position_normalize(value):
    value = max(value, 0)
    value = min(value, 100)
    return value


class Window(Switch):
    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, reverse=False, priority_mode=False, allow_unknown=False):
        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.reverse = reverse
        self.entity_init()

    def position(self):
        dct = self.attrs()
        output = dct.get('current_position', dct.get('position'))
        if output is not None and self.reverse:
            output = 100 - int(output)
        return output

    def position_set(self, value):
        log.debug(f"Setting {self.entity} {self.friendly_name()} position to {value}")
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


class Cover(Window):
    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, reverse=False, priority_mode=False, allow_unknown=False):
        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.reverse = reverse
        self.entity_init()
