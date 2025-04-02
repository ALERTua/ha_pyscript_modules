# https://github.com/custom-components/pyscript
from imports_base import *
import common_tools as tools
from entities.ha import HA
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
import homeassistant.helpers.template as template
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/entity.py
import homeassistant.helpers.entity as entity_helper
from homeassistant.components.recorder import get_instance
from homeassistant.components.recorder.statistics import statistics_during_period
from typing import Literal, Optional
from datetime import datetime, timezone

ha = HA()


def entity(entity_id, debug=False):
    if isinstance(entity_id, Entity):
        return entity_id

    if isinstance(entity_id, str) and entity_id.count('.') > 1:
        entity_id = '.'.join(entity_id.split('.')[:2])

    output = Entity.entity_library.get(entity_id, None)
    if output is not None and isinstance(output, Entity):
        if debug:
            log.debug(f"Returned {entity_id} from library: {type(output)} {output}")
        return output

    if hass.states.get(entity_id) is not None:
        eid = None
        ent = None
        domain = None
        try:
            eid = ha.resolve_entity_id(entity_id)
            ent = ha.get_entity(eid)
            domain = ent.domain
        except Exception as e:
            msg = f"⛔Entity getter failed for\nentity_id: {entity_id}\neid: {eid}\nent: {ent}\nException: {type(e)} {e}"
            # log.debug(msg)

            if debug:
                tools.discord_message(msg, target=['1252277077848359055'])
            # tools.telegram_message_alert_ha_private(msg, disable_notification=True)
            domain = (ent or eid or entity_id).split('.')[0]
    else:
        domain = entity_id.split('.')[0]

    if domain == 'binary_sensor':
        from entities.binary_sensor import BinarySensor
        output = BinarySensor(entity_id)
    elif domain == 'climate':
        from entities.climate import Climate
        output = Climate(entity_id)
    elif domain == 'light':
        from entities.light import Light
        output = Light(entity_id)
    elif domain == 'media_player':
        from entities.media_player import MediaPlayer
        output = MediaPlayer(entity_id)
    elif domain == 'sensor':
        from entities.sensor import Sensor
        output = Sensor(entity_id)
    elif domain in ('switch', 'input_boolean', 'fan'):
        from entities.switch import Switch
        output = Switch(entity_id)
    elif domain == 'cover':
        from entities.window import Cover
        output = Cover(entity_id)
    elif domain == 'number':
        from entities.number import Number
        output = Number(entity_id)
    elif domain == 'water_heater':
        from entities.water_heater import WaterHeater
        output = WaterHeater(entity_id)
    elif domain == 'lock':
        from entities.lock import Lock
        output = Lock(entity_id)
    elif domain == 'notify':
        from entities.companion import Companion
        output = Companion(entity_id)
    elif domain == 'select':
        from entities.select import Select
        output = Select(entity_id)
    else:
        output = Entity(entity_id)

    if domain not in ('notify',):
        Entity.entity_library[entity_id] = output
        Entity.entity_registry.add(entity_id)
    # log.debug(f"Added {output.__repr__()} to library")
    return output


def entity_latest_changed(*entity_ids, debug=True):
    entities = list([entity(_) for _ in entity_ids])
    output = {}
    for e in entities:
        output[e.entity_id] = e.last_changed()

    output = dict(sorted(output.items(), key=lambda item: item[1], reverse=True))

    if debug:
        log.debug(f"entity_latest:\n{output}")

    output = list(output.keys())[0]
    output = entity(output)
    return output


def entity_latest_updated(*entity_ids, debug=False):
    entities = list([entity(_) for _ in entity_ids])
    output = {}
    for e in entities:
        output[e.entity_id] = e.last_changed()

    output = dict(sorted(output.items(), key=lambda item: item[1], reverse=True))

    if debug:
        log.debug(f"entity_latest:\n{output}")

    output = list(output.keys())[0]
    output = entity(output)
    return output


class Entity:
    entity_registry = set()
    entity_library = dict()

    # noinspection PyMissingConstructor
    def __init__(self, entity_id: str):
        self.entity_id: str = entity_id
        self.init()

    # noinspection PyArgumentList
    @pyscript_compile
    def __eq__(self, other):
        return isinstance(other, Entity) and self.entity_id == other.entity_id

    # noinspection PyArgumentList
    @pyscript_compile
    def __str__(self):
        return self.entity_id

    # noinspection PyArgumentList
    @pyscript_compile
    def __repr__(self):
        return f"[{self.__class__.__name__}]({self.entity_id})"

    # noinspection PyAttributeOutsideInit
    def init(self):
        self.entity_domain, self.entity_name = self.entity_id.split('.')
        if getattr(self, 'ha_state', None) is None:
            self.ha_state = template.TemplateStateFromEntityId(hass, self.entity_id)

    def attrs(self) -> Dict:
        return self.ha_state.attributes

    def setattr(self, name, value):
        attrs = self.attrs()
        # log.debug(f"{self.entity_id} attrs before:\n{pformat(attrs)}")
        new_dict = {k: v for k, v in attrs.items()}
        new_dict[name] = value
        state.set(self.entity_id, new_attributes=new_dict)
        # attrs = self.attrs()
        # log.debug(f"{self.entity_id} attrs after:\n{pformat(attrs)}")

    def delattr(self, name):
        attrs = self.attrs()
        # log.debug(f"{self.entity_id} attrs before:\n{pformat(attrs)}")
        new_dict = {k: v for k, v in attrs.items() if k != name}
        state.set(self.entity_id, new_attributes=new_dict)
        # attrs = self.attrs()
        # log.debug(f"{self.entity_id} attrs after:\n{pformat(attrs)}")

    def exists(self) -> bool:
        return state.exist(self.entity_id)

    def exist(self):
        return self.exists()

    def as_dict(self) -> Dict:
        return self.ha_state.as_dict()

    def domain(self) -> str:
        return self.ha_state.domain

    def area(self):
        return self.ha_state.object_id

    def as_str(self):
        return f"[{self.__class__.__name__}]({self.entity_id}){self.friendly_name()}"

    def friendly_name(self):
        return self.attrs().get('friendly_name')

    def state(self, attr=None, default=None):
        if attr:
            return self.attrs().get(attr, default)

        try:
            return self.ha_state.state
        except:
            eid = self.entity_id
            return state.get(eid)

    def state_translated(self):
        return template.StateTranslated(hass)(self.entity_id)

    def is_on(self):
        return self.state() == 'on'

    def is_not_on(self):
        return not self.is_on()

    def is_off(self):
        return self.state() == 'off'

    def is_not_off(self):
        return not self.is_off()

    def is_on_str(self):
        return f"({self.entity_id} == 'on')"

    def is_off_str(self):
        return f"({self.entity_id} == 'off')"

    def is_not_on_str(self):
        return f"({self.entity_id} != 'on')"

    def is_not_off_str(self):
        return f"({self.entity_id} != 'off')"

    def is_unavailable(self):
        _state = self.state()
        return _state == 'unavailable'

    def is_unknown(self):
        _state = self.state()
        return _state == 'unknown'

    def config_entry_id(self):
        if self.ha_state is None:
            return

        return template.config_entry_id(hass, self.entity_id)

    def device_id(self):
        if self.ha_state is None:
            return

        return template.device_id(hass, self.entity_id)

    def device(self):
        if device_id := self.device_id():
            from entities.device import Device
            return Device(device_id)

    def device_entities(self):
        if self.ha_state is None:
            return

        return template.device_entities(hass, self.device_id())

    def last_changed(self) -> datetime:
        last_changed = self.ha_state.last_changed
        return tools.dt_from_timestamp(last_changed)

    def last_updated(self) -> datetime:
        last_updated = self.ha_state.last_updated
        return tools.dt_from_timestamp(last_updated)

    def area_id(self):
        return template.area_id(hass, self.entity_id)

    def area_name(self):
        return template.area_name(hass, self.entity_id)

    def capability(self, capability):
        return entity_helper.get_capability(hass, self.entity_id, capability)

    def device_class(self):
        return entity_helper.get_device_class(hass, self.entity_id)

    def supported_features(self):
        return entity_helper.get_supported_features(hass, self.entity_id)

    def unit_of_measurement(self):
        return entity_helper.get_unit_of_measurement(hass, self.entity_id)

    async def get_history(
            self,
            start_time: datetime,
            end_time: Optional[datetime],
            period: Literal["5minute", "day", "hour", "week", "month"],
            types: Literal["last_reset", "max", "mean", "min", "state", "sum"]):
        """
        start_time = datetime.today().replace(day=1)
        end_time = datetime.today()

        history = _get_history(start_time, end_time, [var_name], "hour", "state")

        for hour in history.get(var_name):
            log.debug(hour)
        """
        start_time = start_time.astimezone(timezone.utc)
        end_time = end_time or ha.datetime()
        end_time = end_time.astimezone(timezone.utc)

        entity_id = self.entity_id
        if not entity_id:
            log.error(f"No Cannot get history. entity_id empty for {self}")
            return

        entity_ids = [entity_id]
        log.debug(f"Getting {types} {period} history for {entity_ids}: {start_time} to {end_time}")
        output = await get_instance(hass).async_add_executor_job(
            statistics_during_period, hass, start_time, end_time, entity_ids, period, None, types)

        if output:
            return output.get(entity_id)
