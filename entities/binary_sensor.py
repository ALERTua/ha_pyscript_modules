# https://github.com/custom-components/pyscript
from entities.entity import Entity


class BinarySensor(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, priority_mode=False, allow_unknown=False):
        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.entity_init()
