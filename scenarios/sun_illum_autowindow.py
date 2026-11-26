from imports import *

# Light and heat conditions of the sun-controlled covers, and the light triggers.
# The office lux sensor stands for the whole facade. The forecast lags the sky, so it counts
# only while WEATHER_SWITCH is on.

ILLUMINATION_SENSOR = OFFICE_ILLUMINATION_SENSOR
ILLUMINATION_CLOUDY = 2521  # lux at or below this value: no direct sun
ILLUMINATION_SUNNY = 2850  # lux at or above this value: direct sun
# Seconds the light must stay past a limit before the light state changes. The sensor sends
# one reading a minute, so CLOUDY_HOLD = 150 needs three low readings in a row, and one short
# shadow does not open the covers.
CLOUDY_HOLD = 10
SUNNY_HOLD = 5
WEATHER_SWITCH = 'input_boolean.sun_autowindow_weather'
WEATHER_CLOUD_COVERAGE = f'{WEATHER_EID}.cloud_coverage'
CLOUD_COVERAGE_LIMIT = 90  # percent of forecast cloud coverage above which it is cloudy
OUTSIDE_TEMPERATURE_SENSOR = 'sensor.officeac_outside_temperature'
HOT_TEMPERATURE = 28  # degrees C outside at or above which the covers close to their limit

# Light switch of each window. While it is off, no direct sun does not open that cover, and the
# cover follows only the sun and the heat.
ILLUM_SWITCHES = {
    'office': 'input_boolean.sun_office_illum_autowindow',
    'kitchen': 'input_boolean.sun_kitchen_illum_autowindow',
    'bedroom': 'input_boolean.sun_bedroom_illum_autowindow',
    'room': 'input_boolean.sun_room_illum_autowindow',
}

# Active time of all cover triggers. END is after the latest summer sunset in the window (21:05).
START = "13:30"
END = "21:30"
RANGE = f"range({START}, {END})"

# Light state with hysteresis. Only the light triggers below change it, after their hold time.
# A reload takes it from the current reading in sun_light_state_on_load.
_light = {'sunny': True}


def state_of(entity_id):
    """State of the entity, or None when Home Assistant has no such entity."""
    try:
        return state.get(entity_id)
    except NameError:
        return None


def number_or_none(value):
    """float(value), or None for None, 'unavailable' and other text."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def in_range():
    """True between START and END, the same time as RANGE."""
    return START <= datetime.now().strftime('%H:%M') < END


def cloudy_by_weather():
    """True when WEATHER_SWITCH is on and the forecast cloud coverage is above the limit."""
    if state_of(WEATHER_SWITCH) != 'on':
        return False
    coverage = number_or_none((state.getattr(WEATHER_EID) or {}).get('cloud_coverage'))
    return coverage is not None and coverage > CLOUD_COVERAGE_LIMIT


def is_cloudy():
    """True when no direct sun hits the facade."""
    return not _light['sunny'] or cloudy_by_weather()


def illum_enabled(key):
    """False only when the light switch of the window is 'off'; a missing switch counts as on."""
    return state_of(ILLUM_SWITCHES[key]) != 'off'


def is_hot():
    """True when the outside temperature is at or above HOT_TEMPERATURE."""
    temperature = number_or_none(state_of(OUTSIDE_TEMPERATURE_SENSOR))
    return temperature is not None and temperature >= HOT_TEMPERATURE


def update_covers():
    # imported here because scenarios.sun_autowindow imports this module
    from scenarios.sun_autowindow import update_all

    update_all()


def set_light(sunny):
    """Store a new light state and, between START and END, update every cover at once."""
    if _light['sunny'] == sunny:
        return
    _light['sunny'] = sunny
    log.debug(f"sun_illum_autowindow: light is now {'sunny' if sunny else 'cloudy'}")
    if in_range():
        update_covers()


@time_trigger('startup')
def sun_light_state_on_load():
    """Take the light state from the current reading; a reading between the limits counts as sunny."""
    lux = number_or_none(state_of(ILLUMINATION_SENSOR))
    _light['sunny'] = lux is None or lux > ILLUMINATION_CLOUDY


# A cloud or the sun coming out changes the light faster than the sun moves, so these
# triggers update every cover at once. They run all day, so that the light state is right
# at START. state_hold_false=0 fires a trigger only when its condition becomes true, not on
# every new reading while it stays true. A reading past the limit before the hold time ends
# cancels the trigger.
@state_trigger(
    f"float_({ILLUMINATION_SENSOR}, default={ILLUMINATION_CLOUDY} + 1) <= {ILLUMINATION_CLOUDY}",
    state_hold=CLOUDY_HOLD,
    state_hold_false=0,
)
def sun_light_cloudy(**kwargs):
    set_light(False)


@state_trigger(
    f"float_({ILLUMINATION_SENSOR}, default={ILLUMINATION_SUNNY} - 1) >= {ILLUMINATION_SUNNY}",
    state_hold=SUNNY_HOLD,
    state_hold_false=0,
)
def sun_light_sunny(**kwargs):
    set_light(True)


@state_trigger(WEATHER_SWITCH)
@state_trigger(WEATHER_CLOUD_COVERAGE)
@time_active(RANGE)
def sun_illum_autowindow(var_name=None, value=None, old_value=None, **kwargs):
    log.debug(f"sun_illum_autowindow: {var_name}: {old_value} -> {value}, updating the covers")
    update_covers()
