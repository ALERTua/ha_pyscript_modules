from imports import *
from entities.entity import Entity
import pickle
from urllib.parse import quote as urlquote

class RingerMode:
    NORMAL = "normal"
    SILENT = "silent"
    VIBRATE = "vibrate"



def companion_actions_dict(*actions: tuple[str, str, str]):
    actions_kw = []
    acitons_actions_kw = {}
    for action_name, action_title, action_actions in actions:
        actions_kw.append(dict(action=action_name, title=action_title))
        acitons_actions_kw[action_name] = action_actions

    acitons_actions_kw_str = pickle.dumps(acitons_actions_kw)
    acitons_actions_kw_str_encoded = urlquote(acitons_actions_kw_str, safe='')

    output = {
        'actions': actions_kw,
        'intent_extras': acitons_actions_kw_str_encoded,
    }
    # log.debug(f"{__name__} actions:\n{pformat(kw)}")
    return output


class Companion(Entity):
    """
    https://companion.home-assistant.io/docs/notifications/notification-commands
    """
    RingerMode = RingerMode
    companion_actions_dict = companion_actions_dict

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
        # self.message(message=f"Ringer mode: {ringer_mode}")

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
        # self.message(message=f"DND: {dnd}")

    def message(self, message: str, title: str = '', **kwargs):
        # https://companion.home-assistant.io/docs/notifications/notification-attachments
        # https://companion.home-assistant.io/docs/notifications/notification-commands/
        """
        subject: "Subject for long text"
        color: "#2DF56D" # or "red"
        sticky: "true" # or "false"
        channel: "Motion" # Name of the channel you wish to create or utilize
        importance: high
        vibrationPattern: "100, 1000, 100, 1000, 100" # The pattern you wish to set for vibrations
        ledColor: "red" # Set the LED to red
        timeout: 10 # How many seconds the notification should be received by the device
        visibility: public
        tts_text: "Motion has been detected"
        media_stream: "alarm_stream_max"
        notification_icon: "mdi:cellphone"
        intent_package_name: "com.urbandroid.sleep"
        intent_extras: "MAX_RAW_DATA:0.2;0.2;0.4;0.3;5.4;6.8;1.2:float[]"
        intent_action: "com.urbandroid.sleep.watch.DATA_UPDATE"
        actions:
          - action: action_open
            title: Open
          - action: action_close
            title: Close
        """
        return self._call(title=title, message=message, data=kwargs)

    def actions(
            self,
            message: str,
            title: str = '',
            *actions: tuple[str, str, str],
            **kwargs,
    ):
        """
            comp = entity(COMPANION_ALERT)
            action_close = '''log.debug('actions_close before 3 sec wait')
task.sleep(3)
log.debug('actions_close after 3 sec wait')'''
            action_open = '''log.debug('action_open before 3 sec wait')
task.sleep(3)
log.debug('action_open after 3 sec wait')'''

            actions = (
                ('action_open', 'Open', action_open),
                ('action_close', 'Close', action_close),
            )

            comp.actions('actions message', 'actions title', *actions)

        """
        kwargs.update(companion_actions_dict(*actions))
        kw = dict(message=message, title=title, **kwargs)
        log.debug(f"companion acitons: {self.entity_domain=} {self.entity_name=} actions:\n{pformat(kw)}")
        return self.message(**kw)

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
