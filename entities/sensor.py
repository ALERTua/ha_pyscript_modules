# https://github.com/custom-components/pyscript
from entities.entity import Entity


class Sensor(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()
