# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
HOLD_1M = 60
HOLD_2M = HOLD_1M * 2
HOLD_3M = HOLD_1M * 3
HOLD_5M = HOLD_1M * 5
HOLD_10M = HOLD_1M * 10
HOLD_15M = HOLD_1M * 15
HOLD_30M = HOLD_1M * 30
HOLD_1H = HOLD_30M * 2
HOLD_2H = HOLD_1H * 2
HOLD_3H = HOLD_1H * 3
HOLD_4H = HOLD_2H * 2
HOLD_5H = HOLD_1H * 5
HOLD_6H = HOLD_3H * 2
HOLD_8H = HOLD_4H * 2
HOLD_10H = HOLD_5H * 2
HOLD_12H = HOLD_6H * 2
HOLD_1D = HOLD_12H * 2
HOLD_2D = HOLD_1D * 2
HOLD_3D = HOLD_1D * 3
HOLD_1W = HOLD_1D * 7

QUIET_HOURS_START = 22
QUIET_HOURS_END = 8

UPTIME = 'sensor.ha_uptime_seconds'

# "cron(min hr dom mon dow)"
TIME_TRIGGER_HOURLY = 'cron(0 * * * *)'
TIME_TRIGGER_DAILY = 'cron(0 12 * * *)'
TIME_TRIGGER_EVERY_MINUTE = 'cron(* * * * *)'

SHOWER_HUMIDITY = 'sensor.shower_humidity_latest'
SHOWER_TEMPERATURE = 'sensor.shower_temperature_latest'
SHOWER_FAN = 'switch.shower_vents_l1'
SHOWER_FAN_SLOW = 'switch.shower_vents_l2'
SHOWER_SPEAKER = 'media_player.mass_shower_speaker'
SHOWER_FLOOR = 'climate.shower_floor'

BATHROOM_FAN = 'fan.bathroom'
BATHROOM_SPEAKER = 'media_player.mass_bathroom_speaker'
BATHROOM_TEMPERATURE = 'sensor.bathroom_temperature_latest'
BATHROOM_HUMIDITY = 'sensor.bathroom_humidity_latest'

BEDROOM_TEMPERATURE = 'sensor.bedroom_temperature_latest'
BEDROOM_HUMIDITY = 'sensor.bedroom_humidity_latest'
BEDROOM_TVOC = 'sensor.bedroom_tvoc_latest'
BEDROOM_PM25 = 'sensor.bedroom_pm25_latest'
BEDROOM_PM10 = 'sensor.bedroom_pm10_latest'
BEDROOM_CO2 = 'sensor.bedroom_co2_latest'
BEDROOM_AC = 'climate.ac_bedroom'
BEDROOM_AUTO_AC = 'input_boolean.bedroom_auto_ac'
BEDROOM_SPEAKER = 'media_player.mass_bedroom_speaker'
BEDROOM_HUMIDIFIER = 'switch.bedroom_humidifier'
BEDROOM_HUMIDIFIER_POWER = 'sensor.bedroom_humidifier_power'
BEDROOM_DIMMER = 'light.miboxer_tl'
BEDROOM_LED_BOTTOM = 'light.bedroom_led_bottom'
BEDROOM_LED_TOP = 'light.bedroom_led_top'

BEDROOM_WINDOW = 'cover.bedroom_window_tl'
BEDROOM_WINDOW_CLOUD = 'cover.bedroom_window_tl'
BEDROOM_WINDOW_REED = 'binary_sensor.bedroom_window_reed_contact'
BEDROOM_WANTED_TEMP = 'input_number.bedroom_wanted_temperature'
BEDROOM_ALLOWED_MODES = 'input_select.bedroom_auto_ac_allowed_modes'
BEDROOM_VALVE = 'climate.valve_bedroom'
BEDROOM_AUTOVALVE_IB = 'input_boolean.bedroom_auto_valve'
BEDROOM_VALVE_POSITION = 'sensor.valve_bedroom_position'

OFFICE_HUMIDIFIER = 'switch.office_humidifier'
OFFICE_HUMIDIFIER_POWER = 'sensor.office_humidifier_power'
OFFICE_HUMIDITY = 'sensor.office_humidity_latest'
OFFICE_TEMPERATURE = 'sensor.office_temperature_latest'
OFFICE_WANTED_TEMP = 'input_number.office_wanted_temperature'
OFFICE_CO2 = 'sensor.office_co2_latest'
OFFICE_WINDOW = 'cover.office_window_tl'
# OFFICE_WINDOW_CLOUD = 'cover.office_window_cloud'
OFFICE_AUDIO = 'media_player.mass_office_audio'
OFFICE_SPEAKER = 'media_player.mass_office_speaker'
# OFFICE_SPEAKER = 'media_player.mass_office_audio'
OFFICE_AC = 'climate.ac_office'
OFFICE_AUTO_AC = 'input_boolean.office_auto_ac'
OFFICE_LIGHTS = 'light.office'
OFFICE_VALVE = 'climate.valve_office'
OFFICE_AUTOVALVE_IB = 'input_boolean.office_auto_valve'
OFFICE_VALVE_POSITION = 'sensor.valve_office_position'
OFFICE_ILLUMINATION_SENSOR = 'sensor.motion_office_sun_illuminance'

ROOM_HUMIDIFIER = 'switch.room_humidifier'
# ROOM_HUMIDIFIER_CLOUD = 'switch.room_humidifier_cloud'
ROOM_HUMIDITY = 'sensor.room_humidity_latest'
ROOM_TEMPERATURE = 'sensor.room_temperature_latest'
ROOM_VALVE_POSITION = 'sensor.valve_room_position'
ROOM_WANTED_TEMP = 'input_number.room_wanted_temperature'
ROOM_WINDOW = 'cover.room_window_tl'
ROOM_WINDOW_REED = 'binary_sensor.room_window_reed_contact'
ROOM_WINDOW_CLOUD = 'cover.room_window_cloud'
ROOM_AUDIO = 'media_player.mass_room_audio'
# ROOM_SPEAKER = 'media_player.mass_room_speaker'
ROOM_SPEAKER = ROOM_AUDIO
ROOM_AC = 'climate.ac_room'
ROOM_AUTO_AC = 'input_boolean.room_auto_ac'
ROOM_VALVE = 'climate.valve_room'
ROOM_AUTOVALVE_IB = 'input_boolean.room_auto_valve'
ROOM_LIGHT = 'light.room'

KITCHEN_WINDOW = 'cover.kitchen_window_tl'
# KITCHEN_WINDOW_CLOUD = 'cover.kitchen_window_cloud'
KITCHEN_SPEAKER = 'media_player.mass_kitchen_speaker'
KITCHEN_AUDIO = 'media_player.mass_kitchen_audio'
KITCHEN_AC = 'climate.ac_kitchen'
KITCHEN_AUTO_AC = 'input_boolean.kitchen_auto_ac'
KITCHEN_HUMIDITY = 'sensor.kitchen_humidity_latest'
KITCHEN_TEMPERATURE = 'sensor.kitchen_temperature_latest'
KITCHEN_WANTED_TEMP = 'input_number.kitchen_wanted_temperature'
KITCHEN_VALVE = 'climate.valve_kitchen'
KITCHEN_AUTOVALVE_IB = 'input_boolean.kitchen_auto_valve'
KITCHEN_VALVE_POSITION = 'sensor.valve_kitchen_position'
KITCHEN_COUCH_LED = 'light.couch_led'
KITCHEN_LIGHT_TOP = 'light.kitchen'
KITCHEN_COUNTERTOP_LED = 'light.kitchen_led'
PROJECTOR = 'switch.projector'
LIGHT_HALLWAY = 'light.hallway'
LIGHT_ENTRANCE = 'light.entrance'

LAUNDRY_HUMIDITY = 'sensor.laundry_humidity_latest'
LAUNDRY_TEMPERATURE = 'sensor.laundry_temperature_latest'
LAUNDRY_VENTS = 'fan.laundry'
LAUNDRY_LIGHT = 'light.laundry'
LAUNDRY_VALVE_COLD = 'switch.valve_cold'
GROUP_LEAK = 'group.water_leak_group'
GROUP_VALVES = 'group.water_valves'
SERVER_TEMPERATURE = 'sensor.alert_server_package_id_0_temperature'
MINI_TEMPERATURE = 'sensor.mini_package_id_0_temperature'
SERVER_RAM_USED_PERCENT = 'sensor.server_ram_used_percent'
BOILER = 'water_heater.boiler'
LAUNDRY_SPEAKER = 'media_player.mass_microusb_speaker'
LAUNDRY_DELTA_2_PLUG = 'switch.delta_2_plug_4'

LIGHT_SHOWER_TOP = 'light.shower'
LIGHT_SHOWER_LED = 'light.shower_led'
LIGHT_MAIN = 'light.main_switch'
LIGHT_BATHROOM_TOP = 'light.bathroom'
LIGHT_BATHROOM_LED = 'light.bathroom_led'

SOMEONE_HOME = 'binary_sensor.someone_s_home'
CATBIRD_HOME = 'binary_sensor.catbird_s_home'
ALERT_HOME = 'binary_sensor.alert_s_home'


ACTION_CALLBACKS = 'pyscript.action_callbacks'
ALERT_ASLEEP = 'binary_sensor.alert_is_asleep'
CATBIRD_ASLEEP = 'binary_sensor.catbird_is_asleep'
SOMEONE_ASLEEP = 'binary_sensor.someone_is_asleep'
HALLWAY_GATEWAY_LUMEN = 'sensor.xiaomi_gateway_illumination'
GATEWAY_V2_MAC = '04:CF:8C:9D:06:61'
# HALLWAY_SPEAKER = 'media_player.hallway_speaker'
SERVER_AVAILABLE_SENSOR = 'binary_sensor.alert_server_web'

LOCK = 'lock.door'

# https://github.com/adrgumula/HomeAssitantBluetoothSpeaker?tab=readme-ov-file
# LAUNDRY_BT_SPEAKER = 'media_player.bs_3'  # 15:08:01:24:08:1A
MUSIC_SPEAKER = 'media_player.mass_music_speakers'
RELAX_SPEAKER = 'media_player.mass_relax'
HA_SPEAKER = 'media_player.mass_mini'
CHROMECAST_BROADCAST = 'media_player.mass_broadcast'
CHROMECAST_ALL_SPEAKERS = 'media_player.mass_all_speakers'
LIST_BROADCAST_SPEAKERS = [
    LAUNDRY_SPEAKER,
    OFFICE_SPEAKER,
    ROOM_SPEAKER,
    KITCHEN_SPEAKER,
    BATHROOM_SPEAKER,
    BEDROOM_SPEAKER,
    SHOWER_SPEAKER,
]

LIST_AC = [
    BEDROOM_AC,
    OFFICE_AC,
    KITCHEN_AC,
    ROOM_AC
]
LIST_AUTO_AC = [
    BEDROOM_AUTO_AC,
    OFFICE_AUTO_AC,
    KITCHEN_AUTO_AC,
    ROOM_AUTO_AC,
]

HUMIDIFIERS = [
    OFFICE_HUMIDIFIER,
    # OFFICE_HUMIDIFIER_CLOUD,
    ROOM_HUMIDIFIER,
    # ROOM_HUMIDIFIER_CLOUD,
    BEDROOM_HUMIDIFIER,
    # BEDROOM_HUMIDIFIER_CLOUD,
]

TEST_BOOLEAN = 'input_boolean.test_boolean'

EMPTY_SOUND = 'silence-1sec.mp3'
MEDIA_CONTENT_TYPE = 'audio/mp3'


def SECRET(value):
    # noinspection PyUnresolvedReferences
    return pyscript.config.get('secrets', {}).get(value)


TELEGRAM_ALERT_ID = SECRET('telegram_alert_id')

TELEGRAM_CHAT_ALERT_HA = SECRET('telegram_chat_alert_ha')
TELEGRAM_TOPIC_ALERT_HA_URGENT = SECRET('telegram_chat_alert_ha_public_topic_urgent')

TELEGRAM_CHAT_ALERT_HA_PRIVATE = SECRET('telegram_chat_alert_ha_private')
TELEGRAM_CHAT_ALERT_VIDEO = SECRET('telegram_chat_alert_video')
DISCORD_CHANNEL_HA = SECRET('discord_channel_ha')
SERVER_URL_EXTERNAL = SECRET('server_url_external')

ROUTER_USERNAME = SECRET('router_username')
ROUTER_PASSWORD = SECRET('router_password')
ROUTER_URL = SECRET('router_url')
UISP_URL = SECRET('uisp_url')
UISP_TOKEN = SECRET('uisp_token')

UNRAID_SSH_HOST = SECRET('unraid_ssh_host')
UNRAID_SSH_PORT = SECRET('unraid_ssh_port')
UNRAID_SSH_USERNAME = SECRET('unraid_ssh_username')
UNRAID_SSH_PASSWORD = SECRET('unraid_ssh_password')
UNRAID_SSH_KEY_PATH = SECRET('unraid_ssh_key_path')

UNRAID_MINI_SSH_HOST = SECRET('unraid_mini_ssh_host')
UNRAID_MINI_SSH_PORT = SECRET('unraid_mini_ssh_port')
UNRAID_MINI_SSH_USERNAME = SECRET('unraid_ssh_mini_username')
UNRAID_MINI_SSH_PASSWORD = SECRET('unraid_ssh_mini_password')
UNRAID_MINI_SSH_KEY_PATH = SECRET('unraid_ssh_mini_key_path')

FRIGATE_URL = SECRET('frigate_url')

XIAOMI_HUB_MAC = SECRET('xiaomi_hub_mac')

OUTAGE_CALENDAR_EID = 'calendar.yasno_group_3_outages_calendar'
NEXT_OUTAGE_DATETIME_EID = 'input_datetime.next_outage_datetime'
POWER_OUTAGE_IB = 'input_boolean.power_outage_calendar'
POWER = POWER_SENSOR = 'binary_sensor.power'
INTERNET = INTERNET_SENSOR = 'binary_sensor.internet'
ALARM_SENSOR_ID = 'binary_sensor.kyiv_alarm'
LLM_STANDARD = "conversation.llm"
# SENSOR_DATETIME = 'sensor.datetime_full'

COMPANION_ALERT = 'notify.mobile_app_alert_s_s24'
COMPANION_TABLET = 'notify.mobile_app_alert_s_redmi_pad_pro'
COMPANION_CATBIRD = 'notify.mobile_app_kateryna_drozd'
GUESTS_IB = 'input_boolean.guests'
