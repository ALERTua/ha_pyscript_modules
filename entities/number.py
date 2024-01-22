# https://github.com/custom-components/pyscript
from imports_base import *
from entities.entity import Entity


class Number(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def set_value(self, value):
        return number.set_value(entity_id=self.entity_id, value=value)
