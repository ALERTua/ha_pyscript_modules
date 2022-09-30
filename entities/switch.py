# https://github.com/custom-components/pyscript
from entities.entity import Entity


class Switch(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, priority_mode=False, allow_unknown=False):
        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.entity_init()

    def turn_on(self, **kwargs):
        # noinspection PyUnresolvedReferences
        return homeassistant.turn_on(entity_id=self.entity_id, **kwargs)

    def turn_off(self, **kwargs):
        # noinspection PyUnresolvedReferences
        return homeassistant.turn_off(entity_id=self.entity_id, **kwargs)

    def toggle(self, **kwargs):
        # noinspection PyUnresolvedReferences
        return homeassistant.toggle(entity_id=self.entity_id, **kwargs)
