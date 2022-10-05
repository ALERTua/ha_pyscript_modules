# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *

HOLD_1M = 60
HOLD_5M = HOLD_1M * 5
HOLD_10M = HOLD_1M * 10
HOLD_30 = HOLD_1M * 30
HOLD_1H = HOLD_1M * 60
HOLD_2H = HOLD_1H * 2
HOLD_3H = HOLD_1H * 3
QUIET_HOURS_START = 22
QUIET_HOURS_END = 8

SHOWER_HUMIDITY = 'sensor.shower_humidity_template'
SHOWER_FAN = 'fan.shower'
SHOWER_SPEAKER = 'media_player.shower_speaker'

BATHROOM_HUMIDITY = 'sensor.ble_bathroom_humidity'
BATHROOM_FAN = 'fan.bathroom'
BATHROOM_SPEAKER = 'media_player.bathroom_speaker'

BEDROOM_TEMPERATURE = 'sensor.bedroom_temperature'
BEDROOM_HUMIDITY = 'sensor.bedroom_humidity'
BEDROOM_TVOC = 'sensor.bedroom_tvoc'
BEDROOM_PM25 = 'sensor.bedroom_pm25'
BEDROOM_CO2 = 'sensor.bedroom_co2'
BEDROOM_AC = 'climate.ac_bedroom'
BEDROOM_AC_SMART = 'climate.bedroom_smart_thermostat'

PC_ALERT = 'switch.wol_alert_pc'
OFFICE_HUMIDIFIER = 'switch.office_humidifier'
OFFICE_HUMIDIFIER_CLOUD = 'switch.office_humidifier_cloud'
OFFICE_HUMIDITY = 'sensor.office_humidity'
OFFICE_TEMPERATURE = 'sensor.office_temperature_template'
OFFICE_WINDOW = 'cover.office_window'
OFFICE_WINDOW_CLOUD = 'cover.office_window_cloud'
OFFICE_SPEAKER = 'media_player.office_speaker'
OFFICE_AC = 'climate.ac_office'
OFFICE_AC_SMART = 'climate.office_smart_thermostat'
OFFICE_LIGHTS = 'light.office'

PC_ROOM = 'switch.wol_catbird'
ROOM_HUMIDIFIER = 'switch.room_humidifier'
ROOM_HUMIDITY = 'sensor.ble_room_humidity'
ROOM_WINDOW = 'cover.room_window'
ROOM_SPEAKER = 'media_player.room_speaker'
ROOM_AC = 'climate.ac_room'

KITCHEN_WINDOW = 'cover.kitchen_window'
KITCHEN_WINDOW_CLOUD = 'cover.kitchen_window_cloud'
KITCHEN_SPEAKER = 'media_player.kitchen_speaker'
KITCHEN_AC = 'climate.ac_kitchen'

LAUNDRY_HUMIDITY = 'sensor.laundry_humidity_template'
LAUNDRY_TEMPERATURE = 'sensor.laundry_temperature_template'
LAUNDRY_VENTS = 'fan.laundry'
LAUNDRY_VALVE_COLD = 'switch.valve_cold'
GROUP_LEAK = 'group.water_leak_group'
GROUP_VALVES = 'group.water_valves'
SERVER_TEMPERATURE = 'sensor.glances_package_id_0_temperature'

LIGHT_SHOWER_TOP = 'light.shower'
LIGHT_SHOWER_LED = 'light.shower_led'
LIGHT_MAIN = 'light.main_switch'

HALLWAY_GATEWAY_LUMEN = 'sensor.xiaomi_gateway_illumination'
ALL_SPEAKERS = 'media_player.all_speakers'
ALL_SPEAKERS_GROUP = [
    'media_player.shower_speaker',
    'media_player.bedroom_speaker',
    'media_player.office_speaker',
    'media_player.room_speaker',
    'media_player.hallway_speaker',
    'media_player.kitchen_speaker',
    'media_player.shower_speaker',
]
MEDIA_PATH_BASE = Path('/config/www/media')
EXTERNAL_MEDIA_BASE = '/local/media/'

HUMIDIFIERS = [
    OFFICE_HUMIDIFIER,
    OFFICE_HUMIDIFIER_CLOUD,
    ROOM_HUMIDIFIER,
]

TEST_BOOLEAN = 'input_boolean.test_boolean'
UNK_O = ('unavailable', 'unknown', 'null', None, 'none', 'None')
UNK_S = str(UNK_O)

UNK_O_OFF = (*UNK_O, 'off')
UNK_S_OFF = str(UNK_O_OFF)

EMPTY_SOUND = 'silence-1sec.mp3'
MEDIA_CONTENT_TYPE = 'audio/mp3'


def SECRET(value):
    return pyscript.config.get('secrets', {}).get(value)


TELEGRAM_CHAT_ALERT_HA = SECRET('telegram_chat_alert_ha')
TELEGRAM_CHAT_1 = SECRET('telegram_chat_1')
SERVER_URL_EXTERNAL = SECRET('server_url_external')

ROUTER_USERNAME = SECRET('router_username')
ROUTER_PASSWORD = SECRET('router_password')
ROUTER_URL = SECRET('router_url')
UISP_URL = SECRET('uisp_url')
UISP_TOKEN = SECRET('uisp_token')

SENSOR_DATETIME = 'sensor.datetime_full'
