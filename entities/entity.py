# https://github.com/custom-components/pyscript
import logging

from imports_base import *
import common_tools as tools
import constants
from entities.ha import HA
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
import homeassistant.helpers.template as template
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/entity.py
import homeassistant.helpers.entity as entity_helper


def entity_from_id(entity_id):
    # log.debug(f"entity_from_id for {entity_id}")
    return hass.states.get(entity_id) or entity_id


def select_entity_id(*entity_ids, priority_mode=False, allow_unknown=False):
    for entity_id in entity_ids:
        Entity.entity_registry.add(entity_id)

    # log.debug(f"selecting among {entity_ids}")
    alive_entities = [entity_from_id(i) for i in entity_ids if i]
    # log.debug(f"alive_entities: {alive_entities}")
    if allow_unknown is False:
        try:
            alive_entities = [i for i in alive_entities if i and i.state not in UNK_O]
        except Exception as e:
            log.error(f"Error selecting entity id from {entity_ids} with allow_unknown={allow_unknown}: {type(e)} {e}")

    # log.debug(f"alive_entities {alive_entities}")
    if alive_entities:
        if priority_mode is False:
            try:
                alive_entities.sort(key=lambda i: pendulum.from_timestamp(i.last_changed.timestamp()))
            except:
                pass

        output = alive_entities[0]
        # log.debug(f"Priority: {priority_mode} Returning {output}")
        return output


def entity(*args, **kwargs):
    if args is None or len(args) == 0 or args[0] in ('', None):
        raise Exception(f"entity with empty args: {args} {kwargs}")

    entity_ = Entity(*args, **kwargs)
    entity_.entity_init()
    domain = entity_.domain()
    if domain == 'binary_sensor':
        from entities.binary_sensor import BinarySensor
        output = BinarySensor(*args, **kwargs)
    elif domain == 'climate':
        from entities.climate import Climate
        output = Climate(*args, **kwargs)
    elif domain == 'light':
        from entities.light import Light
        output = Light(*args, **kwargs)
    elif domain == 'media_player':
        from entities.media_player import MediaPlayer
        output = MediaPlayer(*args, **kwargs)
    elif domain == 'sensor':
        from entities.sensor import Sensor
        output = Sensor(*args, **kwargs)
    elif domain in ('switch', 'input_boolean', 'fan'):
        from entities.switch import Switch
        output = Switch(*args, **kwargs)
    elif domain == 'cover':
        from entities.window import Cover
        output = Cover(*args, **kwargs)
    elif domain == 'number':
        from entities.number import Number
        output = Number(*args, **kwargs)
    else:
        output = entity_

    entity_.entity_init()
    return output


class Entity:
    entity_registry = set()
    entity = None  # type: State

    # noinspection PyMissingConstructor
    def __init__(self, *entity_ids, priority_mode=False, allow_unknown=False):
        if entity_ids is None or len(entity_ids) == 0 or entity_ids[0] in ('', None):
            raise Exception

        self.entity_ids = entity_ids
        self._priority_mode = priority_mode
        self._allow_unknown = allow_unknown
        self.ha = HA()
        self.entity_init()

    @pyscript_compile
    def __eq__(self, other):
        return isinstance(other, Entity) and self.entity_id == other.entity_id

    # noinspection PyAttributeOutsideInit
    def entity_init(self):
        # noinspection PyTypeChecker
        self.entity = getattr(self, 'entity', None)  # type: State
        self.entity_id = getattr(self, 'entity_id', self._entity_id())

    def _entity_id(self):
        if not any(self.entity_ids):
            return

        output = select_entity_id(*self.entity_ids, priority_mode=self._priority_mode,
                                  allow_unknown=self._allow_unknown)
        # log.debug(f"{self.__class__.__name__} entity_id chosen: "
        #           f"{type(output)} {tools.friendly_name(output.entity_id)} {output}")
        if not output or isinstance(output, str):
            log.error(f"Couldn't find alive entity among {self.entity_ids}")
            return

        self.entity = output  # type: State
        return output.entity_id

    def exists(self):
        return self.entity_id is not None and hass.states.get(self.entity_id) is not None

    def as_str(self):
        friendly_name = self.friendly_name()
        return f"[{self.__class__.__name__}]({self.entity_id}){friendly_name}"

    def friendly_name(self):
        output = tools.friendly_name(self.entity_id)
        return output

    def attrs(self):
        return self.entity.attributes

    def as_dict(self):
        entity_ = self.entity
        output = entity_.as_dict()
        return output

    def state(self, attr=None):
        if not self:
            return None

        if attr:
            return self.attrs().get(attr)

        if self.entity is None:
            return None

        return self.entity.state

    def is_on(self):
        return self.state() == 'on'

    def is_not_on(self):
        return not self.is_on()

    def is_off(self):
        return self.state() == 'off'

    def is_not_off(self):
        return not self.is_off()

    def is_on_str(self):
        return f"{self.entity_id} == 'on'"

    def is_off_str(self):
        return f"{self.entity_id} == 'off'"

    def is_not_on_str(self):
        return f"{self.entity_id} != 'on'"

    def is_not_off_str(self):
        return f"{self.entity_id} != 'off'"

    def domain(self):
        if self.entity is None:
            return

        return self.entity.domain

    def object_id(self):
        if self.entity is None:
            return

        return self.entity.object_id

    def device_id(self):
        if self.entity is None:
            return

        return template.device_id(hass, self.entity_id)

    def device_entities(self):
        if self.entity is None:
            return

        return template.device_entities(hass, self.device_id())

    def template_state(self):
        if self.entity is None:
            return

        # https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py#L880
        # ['__annotations__', '__class__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__',
        # '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__',
        # '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
        # '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__slots__', '__str__', '__subclasshook__',
        # '__weakref__', '_as_dict', '_collect', '_collect_state', '_entity_id', '_hass', '_state', 'as_dict',
        # 'attributes', 'context', 'domain', 'entity_id', 'expire', 'from_dict', 'last_changed', 'last_updated',
        # 'name', 'object_id', 'state', 'state_with_unit']
        return template.TemplateStateFromEntityId(hass, self.entity_id)

    def template(self):
        if self.entity is None:
            return

        return template.expand(hass, self.entity_id)[0]

    def last_changed(self):
        if self.entity is None:
            return

        last_changed = self.entity.last_changed
        return tools.dt_to_pd(last_changed)

    def last_updated(self):
        if self.entity is None:
            return

        last_updated = self.entity.last_updated
        return tools.dt_to_pd(last_updated)

    def area_id(self):
        if self.entity is None:
            return

        return template.area_id(hass, self.entity_id)

    def area_name(self):
        if self.entity is None:
            return

        return template.area_name(hass, self.entity_id)

    def capability(self):
        if self.entity is None:
            return

        return entity_helper.get_capability(hass, self.entity_id)

    def device_class(self):
        if self.entity is None:
            return

        return entity_helper.get_device_class(hass, self.entity_id)

    def supported_features(self):
        if self.entity is None:
            return

        return entity_helper.get_supported_features(hass, self.entity_id)

    def unit_of_measurement(self):
        if self.entity is None:
            return

        return entity_helper.get_unit_of_measurement(hass, self.entity_id)
