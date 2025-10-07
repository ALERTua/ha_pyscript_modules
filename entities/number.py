# https://github.com/custom-components/pyscript
from imports_base import *
from entities.entity import Entity


class Number(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()
        self._old_toggle_state = None

    def set_value(self, value):
        if self.entity_domain == 'input_number':
            return input_number.set_value(entity_id=self.entity_id, value=value)

        return number.set_value(entity_id=self.entity_id, value=value)

    def min(self):
        return self.attrs().get('min', 0)

    def max(self):
        return self.attrs().get('max', 100)

    def step(self):
        return self.attrs().get('step', 1)

    def toggle(self):
        if self._old_toggle_state is not None:
            self.set_value(self._old_toggle_state)
            self._old_toggle_state = None
            return

        _state = self._old_toggle_state = float(self.state())
        _min = float(self.min())
        _max = float(self.max())

        if _state == _min:
            new_state = _max
        elif _state == _max:
            new_state = _min
        else:
            new_state = _state - float(self.step())

        log.debug(f"toggling {self.entity_id} {_state}->{new_state}")
        self.set_value(new_state)
