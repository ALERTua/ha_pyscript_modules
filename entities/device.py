from imports_base import *
from homeassistant.helpers import device_registry


class Device:
    def __init__(self, device_id):
        self.device_id = device_id

    @pyscript_compile
    def __repr__(self):
        return f"Device: {self.device_id}"

    def ha_device(self) -> device_registry.DeviceEntry:
        registry = device_registry.async_get(hass)
        return registry.async_get(self.device_id)

    def disable(self):
        # homeassistant.disable_device(device_id=self.device_id)  # https://spook.boo
        registry = device_registry.async_get(hass)
        registry.async_update_device(device_id=self.device_id, disabled_by=device_registry.DeviceEntryDisabler.USER)

    def enable(self):  # https://spook.boo
        # homeassistant.enable_device(device_id=self.device_id)  # https://spook.boo
        registry = device_registry.async_get(hass)
        registry.async_update_device(device_id=self.device_id, disabled_by=None)

    def disabled(self):
        ha_device = self.ha_device()
        if ha_device is not None:
            return ha_device.disabled_by is not None

    def enabled(self):
        return not self.disabled()