# https://github.com/custom-components/pyscript
from imports_base import *
from entities.switch import Switch


def position_normalize(value):
    value = max(value, 0)
    value = min(value, 100)
    return value


class Window(Switch):
    def __init__(self, entity_id, reverse=False):
        super().__init__(entity_id)
        self.reverse = reverse

    def position(self):
        dct = self.attrs()
        output = dct.get('current_position', dct.get('position'))
        if output is not None and self.reverse:
            output = 100 - int(output)
        return output

    def position_set(self, value):
        value = position_normalize(value)
        # position() already applies reverse, so compare before reversing the target
        if self.position() == value:
            return
        if self.reverse:
            value = 100 - int(value)

        log.debug(f"Setting {self.ha_state} {self.friendly_name()} position to {value}")
        # noinspection PyUnresolvedReferences
        return cover.set_cover_position(entity_id=self.entity_id, position=value)

    def position_add(self, value):
        position = self.position()
        if position is None:
            return None
        new_value = position_normalize(int(position) + value)
        return self.position_set(new_value)

    def position_subtract(self, value):
        return self.position_add(-value)

    def stop(self):
        return cover.stop_cover(entity_id=self.entity_id)

    def open(self):
        return cover.open_cover(entity_id=self.entity_id)

    def close(self):
        return cover.close_cover(entity_id=self.entity_id)


class Cover(Window):
    pass
