# https://github.com/custom-components/pyscript
# https://hacs-pyscript.readthedocs.io/en/stable/
from imports_base import *
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
from homeassistant.helpers import template, device_registry, entity_registry, entity as entity_helper
from entities.device import Device
from zoneinfo import ZoneInfo


class HA:
    def __init__(self):
        self.data = hass.data
        self.config = hass.config

    # def datetime_dt_old(self):
    #     from entities.entity import entity
    #     entity_ = entity(SENSOR_DATETIME)
    #     state_ = entity_.state()
    #     dt = datetime.fromisoformat(state_)
    #     return dt

    @staticmethod
    def dt_from_string(dt_str):
        if dt_str not in (None, 'unknown', 'unavailable'):
            iso = datetime.fromisoformat(dt_str)
            output = dt_util.as_local(iso)
            return output

    def datetime(self):
        return dt_util.now(time_zone=self.time_zone())

    def ip(self):
        return self.config.api.host

    def local_ip(self):
        return self.config.api.local_ip

    def port(self):
        return self.config.api.port

    def use_ssl(self):
        return self.config.api.use_ssl

    def external_url(self):
        return self.config.external_url

    def internal_url(self):
        return self.config.internal_url

    def os_version(self):
        return self.config.version

    def time_zone_str(self):
        return self.config.time_zone

    def time_zone(self):
        return ZoneInfo(self.time_zone_str())

    # noinspection PyMethodMayBeStatic
    def render_template(self, template_, *args, **kwargs):
        """
            returns template.Template("{{ states('light.office') == 'off' }}", hass).async_render()
        """
        tmpl = template.Template(template_, hass)
        result = tmpl.async_render(*args, **kwargs)
        return result

    # noinspection PyMethodMayBeStatic
    def _device_registry(self):
        return device_registry.async_get(hass)

    def ha_devices(self, filter_func=None) -> list[device_registry.DeviceEntry]:
        # duplicates = [_ for __, _ in devices.devices.items() if 'duplicates' in _.labels]
        # duplicates = ha.devices(filter_func=lambda device: 'duplicates' in device.labels)
        registry = self._device_registry()
        output = registry.devices.values()
        if filter_func:
            output = filter(filter_func, output)
        return list(output)

    def devices(self, filter_func=None) -> list[Device]:
        output = self.ha_devices(filter_func=filter_func)
        log.debug(f"Returning {len(output)} devices")
        if output:
            output = [Device(_.id) for _ in output]
        return output

    @staticmethod
    def entity_registry():
        return entity_registry.async_get(hass)

    def get_entity(self, entity_id_or_uuid: str):
        entity_registry_ = self.entity_registry()
        return entity_registry_.async_get(entity_id_or_uuid=entity_id_or_uuid)

    def resolve_entity_id(self, entity_id_or_uuid: str):
        entity_registry_ = self.entity_registry()
        return entity_registry.async_resolve_entity_id(entity_registry_, entity_id_or_uuid)

    def validate_entity_id(self, entity_id_or_uuid: str):
        entity_registry_ = self.entity_registry()
        return entity_registry.async_resolve_entity_id(entity_registry_, entity_id_or_uuid)

    @staticmethod
    def get_device_class(entity_id: str):
        return entity_helper.get_device_class(hass, entity_id)
