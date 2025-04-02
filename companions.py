from constants import *
from entities.companion import Companion

E_ALERT_COMPANION = Companion(
    entity_id=COMPANION_ALERT,
    ringer_mode_eid='sensor.alert_s_s24_ringer_mode',
    battery_level_eid='sensor.alert_s_s24_battery_level',
    battery_level_state_eid='sensor.alert_s_s24_battery_state',
    dnd_eid='sensor.alert_s_s24_do_not_disturb_sensor',
    charging_eid='binary_sensor.alert_s_s24_is_charging',
    public_ip_eid='sensor.alert_s_s24_public_ip_address',
    wifi_bssid_eid='sensor.alert_s_s24_wifi_bssid',
    wifi_ssid_eid='sensor.alert_s_s24_wifi_connection',
    wifi_ip_eid='sensor.alert_s_s24_wifi_ip_address',
)

E_TABLET_COMPANION = Companion(
    entity_id=COMPANION_TABLET,
    ringer_mode_eid='sensor.alert_s_redmi_pad_pro_ringer_mode',
    battery_level_eid='sensor.alert_s_redmi_pad_pro_battery_level',
    battery_level_state_eid='sensor.alert_s_redmi_pad_pro_battery_state',
    dnd_eid='sensor.alert_s_redmi_pad_pro_do_not_disturb_sensor',
    charging_eid='binary_sensor.alert_s_redmi_pad_pro_is_charging',
    public_ip_eid='sensor.alert_s_redmi_pad_pro_public_ip_address',
    wifi_bssid_eid='sensor.alert_s_redmi_pad_pro_wi_fi_bssid',
    wifi_ssid_eid='sensor.alert_s_redmi_pad_pro_wi_fi_connection',
    wifi_ip_eid='sensor.alert_s_redmi_pad_pro_wi_fi_ip_address',
)

E_CATBIRD_COMPANION = Companion(
    entity_id=COMPANION_CATBIRD,
    ringer_mode_eid=None,
    battery_level_eid=None,
    battery_level_state_eid=None,
    dnd_eid='binary_sensor.iphone_kateryna_focus',
    charging_eid=None,
    public_ip_eid=None,
    wifi_bssid_eid='sensor.iphone_kateryna_bssid',
    wifi_ssid_eid='sensor.iphone_kateryna_ssid',
    wifi_ip_eid=None,
)
