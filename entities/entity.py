# https://github.com/custom-components/pyscript
from imports_base import *
import common_tools as tools
import constants
from entities.ha import HA


def entity_from_id(entity_id):
    # log.debug(f"entity_from_id for {entity_id}")
    return hass.states.get(entity_id) or entity_id


def select_entity_id(*entity_ids, priority_mode=False, allow_unknown=False):
    # log.debug(f"selecting among {entity_ids}")
    alive_entities = [entity_from_id(i) for i in entity_ids if i]
    # log.debug(f"alive_entities: {alive_entities}")
    if allow_unknown is False:
        alive_entities = [i for i in alive_entities if i and i.state not in constants.UNK_O]
    # log.debug(f"alive_entities {alive_entities}")
    if alive_entities:
        if priority_mode is False:
            alive_entities.sort(key=lambda i: pendulum.from_timestamp(i.last_changed.timestamp()))
        output = alive_entities[0]
        # log.debug(f"Priority: {priority_mode} Returning {output}")
        return output


def entity(*args, **kwargs):
    entity_ = Entity(*args, **kwargs)
    domain = entity_.domain()
    if domain == 'light':
        from entities.light import Light
        return Light(*args, **kwargs)
    elif domain == 'switch':
        from entities.switch import Switch
        return Switch(*args, **kwargs)
    elif domain == 'sensor':
        from entities.sensor import Sensor
        return Sensor(*args, **kwargs)
    elif domain == 'binary_sensor':
        from entities.binary_sensor import BinarySensor
        return BinarySensor(*args, **kwargs)
    elif domain == 'cover':
        from entities.window import Cover
        return Cover(*args, **kwargs)
    else:
        return entity_


class Entity:
    entity = None  # type: State

    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, priority_mode=False, allow_unknown=False):
        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.ha = HA()
        self.entity_init()

    # noinspection PyAttributeOutsideInit
    def entity_init(self):
        # noinspection PyTypeChecker
        self.entity = None  # type: State
        self.entity_id = self._entity_id()

    def _entity_id(self):
        output = select_entity_id(*self.entity_ids, priority_mode=self._priority_mode,
                                  allow_unknown=self._allow_unknown)
        # log.debug(f"{self.__class__.__name__} entity_id chosen: "
        #           f"{type(output)} {tools.friendly_name(output.entity_id)} {output}")
        if not output:
            log.error(f"Couldn't find alive entity among {self.entity_ids}")
            return

        self.entity = output  # type: State
        return output.entity_id

    def as_str(self):
        return f"[{self.__class__.__name__}]({self.entity_id}){self.friendly_name()}"

    def friendly_name(self):
        return tools.friendly_name(self.entity_id)

    def attrs(self):
        return self.entity.attributes

    def as_dict(self):
        return self.entity.as_dict()

    def state(self, attr=None):
        if attr:
            return self.attrs().get(attr)

        return self.entity.state

    def domain(self):
        return self.entity.domain

    def object_id(self):
        return self.entity.object_id

    def last_changed(self):
        last_changed = self.entity.last_changed
        timestamp = last_changed.timestamp()
        return pendulum.from_timestamp(timestamp)

    def last_updated(self):
        last_changed = self.entity.last_updated
        timestamp = last_changed.timestamp()
        return pendulum.from_timestamp(timestamp)
