# https://github.com/custom-components/pyscript
from entities.entity import Entity


class Switch(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def turn_on(self, **kwargs):
        # noinspection PyUnresolvedReferences
        return homeassistant.turn_on(entity_id=self.entity_id, **kwargs)

    def turn_off(self, **kwargs):
        # noinspection PyUnresolvedReferences
        return homeassistant.turn_off(entity_id=self.entity_id, **kwargs)

    def toggle(self, **kwargs):
        # noinspection PyUnresolvedReferences
        return homeassistant.toggle(entity_id=self.entity_id, **kwargs)

    def turn(self, state_: bool, **kwargs):
        if state_:
            return self.turn_on(**kwargs)
        else:
            return self.turn_off(**kwargs)
