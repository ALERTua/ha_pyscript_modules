# https://github.com/custom-components/pyscript
# https://hacs-pyscript.readthedocs.io/en/stable/
from imports_base import *
from pyscript_mock import *
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
import homeassistant.helpers.template as template


class HA:
    def __init__(self):
        self.data = hass.data
        self.config = hass.config
        self.host_info = hass.components.hassio.get_host_info()
        self.info = hass.components.hassio.get_info()

    def disk_free(self):
        return self.host_info.get('disk_free')

    def disk_total(self):
        return self.host_info.get('disk_total')

    def disk_used(self):
        return self.host_info.get('disk_used')

    def hostname(self):
        return self.host_info.get('hostname')

    def kernel(self):
        return self.host_info.get('kernel')

    def operating_system(self):
        return self.host_info().get('operating_system')

    def datetime_dt_old(self):
        from entities.entity import entity
        entity_ = entity(SENSOR_DATETIME)
        state_ = entity_.state()
        dt = datetime.fromisoformat(state_)
        return dt

    def datetime_dt(self):
        return template.now(hass)

    def datetime_dt_utc(self):
        return template.utcnow(hass)

    def datetime_p(self):
        datetime_dt = self.datetime_dt()
        timestamp = datetime_dt.timestamp()
        tz = self.time_zone_pytz()
        output = pendulum.from_timestamp(timestamp, tz=tz)
        return output

    def boot_timestamp(self):
        return self.host_info.get('boot_timestamp')

    def supervisor_version(self):
        return self.info.get('supervisor')

    def ha_version(self):
        return self.info.get('homeassistant')

    def hassos_version(self):
        return self.info.get('hassos')

    def docker_version(self):
        return self.info.get('docker')

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

    def time_zone_pytz(self):
        from pendulum.tz import Timezone
        return Timezone(hass.config.time_zone)
