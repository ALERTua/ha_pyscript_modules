# https://github.com/custom-components/pyscript
from entities.entity import Entity


class Lock(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def locked(self):
        return self.state() == 'locked'

    def lock(self):
        # noinspection PyUnresolvedReferences
        lock.lock(entity_id=self.entity_id)

    def unlock(self):
        # noinspection PyUnresolvedReferences
        lock.unlock(entity_id=self.entity_id)

    def toggle(self):
        if self.locked():
            self.unlock()
        else:
            self.lock()
