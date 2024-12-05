from imports import *
from entities.entity import Entity

class RingerMode:
    NORMAL = "normal"
    SILENT = "silent"
    VIBRATE = "vibrate"


# TODO: https://companion.home-assistant.io/docs/notifications/actionable-notifications
class Companion(Entity):
    """
    https://companion.home-assistant.io/docs/notifications/notification-commands
    """
    RingerMode = RingerMode

    # noinspection PyMissingConstructor
    def __init__(
            self,
            entity_id: str,
            ringer_mode_eid: str = None,
            battery_level_eid: str = None,
            battery_level_state_eid: str = None,
            dnd_eid: str = None,
            charging_eid: str = None,
            public_ip_eid: str = None,
            wifi_bssid_eid: str = None,
            wifi_ssid_eid: str = None,
            wifi_ip_eid: str = None,
    ):
        self.entity_id = entity_id

        self.ringer_mode_eid = ringer_mode_eid
        self.battery_level_eid = battery_level_eid
        self.battery_level_state_eid = battery_level_state_eid
        self.dnd_eid = dnd_eid
        self.charging_eid = charging_eid
        self.public_ip_eid = public_ip_eid
        self.wifi_bssid_eid = wifi_bssid_eid
        self.wifi_ssid_eid = wifi_ssid_eid
        self.wifi_ip_eid = wifi_ip_eid

        self.init()

    def _call(self, **kwargs):
        # noinspection PyUnresolvedReferences
        return service.call(domain=self.entity_domain, name=self.entity_name, **kwargs)

    def ringer_mode(self, ringer_mode: RingerMode = None):
        if ringer_mode is None and self.ringer_mode_eid:
            return state.get(self.ringer_mode_eid)

        if ringer_mode and self.ringer_mode_eid and ringer_mode == state.get(self.ringer_mode_eid):
            return

        log.debug(f"Setting {self.entity_id} ringer mode to {ringer_mode}")
        self._call(message="command_ringer_mode", data=dict(command=ringer_mode))
        self.message(message=f"Ringer mode: {ringer_mode}")

    def battery_level(self):
        if self.battery_level_eid:
            return state.get(self.battery_level_eid)

    def battery_level_state(self):
        if self.battery_level_state_eid:
            return state.get(self.battery_level_state_eid)

    def charging(self):
        if self.charging_eid:
            return state.get(self.charging_eid)

    def public_ip(self):
        if self.public_ip_eid:
            return state.get(self.public_ip_eid)

    def wifi_bssid(self):
        if self.wifi_bssid_eid:
            return state.get(self.wifi_bssid_eid)

    def wifi_ssid(self):
        if self.wifi_ssid_eid:
            return state.get(self.wifi_ssid_eid)

    def wifi_ip(self):
        if self.wifi_ip_eid:
            return state.get(self.wifi_ip_eid)

    def dnd(self, dnd: Literal["alarms_only", "off", "priority_only", "total_silence"] = None):
        if dnd is None and self.dnd_eid:
            return state.get(self.dnd_eid)

        if dnd is not None and self.dnd_eid is not None and dnd == state.get(self.dnd_eid):
            log.debug(f"{self.entity_id} dnd is already {dnd}")
            return

        log.debug(f"Setting {self.entity_id} dnd to {dnd}")
        self._call(message="command_dnd", data=dict(command=dnd))
        self.message(message=f"DND: {dnd}")

    def message(self, message: str, title: str = '', **kwargs):
        # https://companion.home-assistant.io/docs/notifications/notification-attachments
        return self._call(title=title, message=message, data=kwargs)

    def request_location_update(self):
        return self._call(message="request_location_update")

    def update_sensors(self):
        return self._call(message="command_update_sensors")

    def command_webview(self, path: str):
        # https://companion.home-assistant.io/docs/notifications/notification-commands#webview
        # e.g. "/lovelace/settings"
        return self._call(message="command_webview", data=dict(command=path))

    def volume_level(
            self,
            volume_level_pct: int,
            media_stream: Literal["alarm_stream", "call_stream", "dtmf_stream", "music_stream",
            "notification_stream", "ring_stream", "system_stream"] = None,
    ):
        return self._call(
            message="command_volume_level", data=dict(media_stream=media_stream, command=volume_level_pct)
        )
