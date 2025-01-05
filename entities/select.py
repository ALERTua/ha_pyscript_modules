# https://github.com/custom-components/pyscript
from imports_base import *
from entities.entity import Entity


class Select(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def toggle(self):
        _state = self.state()
        if _state == 'unknown':
            options = self.options()
            if not options:
                log.error(f"Select entity {self.entity_id} has state 'unknown' and no options. Aborting.")
                return

            option = options[0]
            log.info(f"Select entity {self.entity_id} has state 'unknown'. Selecting {option}")
            return self.select(option)

        log.info(f"Select entity {self.entity_id} Selecting next")
        service.call(self.entity_domain, 'select_next', entity_id=self.entity_id, cycle=True)

    def options(self):
        return self.attrs().get('options', [])

    def select(self, option):
        service.call(self.entity_domain, 'select_option', entity_id=self.entity_id, option=option)
