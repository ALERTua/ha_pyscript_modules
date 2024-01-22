# https://github.com/custom-components/pyscript
from entities.switch import Switch


class Light(Switch):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()
