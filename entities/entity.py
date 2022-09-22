# https://github.com/custom-components/pyscript
from imports import *
from entities.ha import HA


def entity_from_id(entity_id):
    return hass.states.get(entity_id) or entity_id


def select_entity_id(*entity_ids, priority_mode=False, allow_unknown=False):
    # log.debug(f"selecting among {entity_ids}")
    alive_entities = [entity_from_id(i) for i in entity_ids]
    # log.debug(f"alive_entities: {alive_entities}")
    if allow_unknown is False:
        alive_entities = [i for i in alive_entities if i.state not in constants.UNK_O]
    # log.debug(f"alive_entities {alive_entities}")
    if alive_entities:
        if priority_mode is False:
            alive_entities.sort(key=lambda i: pendulum.from_timestamp(i.last_changed.timestamp()))
        output = alive_entities[0]
        # log.debug(f"Priority: {priority_mode} Returning {output}")
        return output


class Entity(HA):
    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, priority_mode=False, allow_unknown=False):
        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.entity_init()

    @classmethod
    # @lru_cache(maxsize=32)
    def get(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    # noinspection PyAttributeOutsideInit
    def entity_init(self):
        self.ha_init()
        self.entity = None
        self.entity_id = self._entity_id()

    def _entity_id(self):
        output = select_entity_id(*self.entity_ids, priority_mode=self._priority_mode,
                                  allow_unknown=self._allow_unknown)
        # log.debug(f"{self.__class__.__name__} entity_id chosen: "
        #           f"{type(output)} {tools.friendly_name(output.entity_id)} {output}")
        if not output:
            log.error(f"Couldn't find alive entity among {self.entity_ids}")
            return

        self.entity = output
        return output.entity_id

    def friendly_name(self):
        return tools.friendly_name(self.entity_id)

    def attrs(self):
        return state.getattr(self.entity_id)

    def state(self, attr=None):
        str_ = self.entity_id
        if attr:
            str_ += f".{attr}"
        return state.get(str_)

    def last_changed(self):
        last_changed = self.state('last_changed')
        timestamp = last_changed.timestamp()
        return pendulum.from_timestamp(timestamp)

    def last_updated(self):
        last_changed = self.state('last_updated')
        timestamp = last_changed.timestamp()
        return pendulum.from_timestamp(timestamp)

    def turn_on(self):
        # noinspection PyUnresolvedReferences
        return homeassistant.turn_on(entity_id=self.entity_id)

    def turn_off(self):
        # noinspection PyUnresolvedReferences
        return homeassistant.turn_off(entity_id=self.entity_id)

    def toggle(self, var=False):
        if var:
            log.debug('var')
        # noinspection PyUnresolvedReferences
        return homeassistant.toggle(entity_id=self.entity_id)
