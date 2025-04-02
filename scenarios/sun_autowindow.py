from imports import *
from pyscript_mock import *
from entities.window import Window


WEATHER_ENTITY_ID = 'weather.accuweather'
AZIMUTH_LOW = 210
AZIMUTH_HIGH = 298
ELEVATION_LOW = 0
ELEVATION_HIGH = 59
DEBUG = False


# # EXAMPLE
# ELEVATION = 'sun.sun.elevation'
# AZIMUTH = 'sun.sun.azimuth'
# INPUT_BOOLEAN_OFFICE = 'input_boolean.sun_office_autowindow'
#
# @state_trigger(
#     AZIMUTH,
#     ELEVATION,
#     INPUT_BOOLEAN_OFFICE,
#     OFFICE_WINDOW,
#     state_check_now=True,
#     # state_hold=60,
#     kwargs={
#         'window_entity_id': OFFICE_WINDOW,
#         'reverse': True,
#         'input_boolean': INPUT_BOOLEAN_OFFICE,
#         'position_limit': 90,
#         'position_open': 10,
#     },
# )
# @conditional(
#     entity_on(INPUT_BOOLEAN_OFFICE),
#     entity_exists(OFFICE_WINDOW),
# )
# @time_active("range(8:00, 22:00)")
# def func_sun_office_autowindow(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
#     return sun_autowindow(trigger_type=trigger_type, var_name=var_name, value=value, old_value=old_value,
#                           context=context, **kwargs)


def sun_autowindow(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    window_entity_id = kwargs.get('window_entity_id')
    if not window_entity_id:
        log.info("Cannot _sun_autowindow: no window_entity_id")
        return

    reverse = kwargs.get('reverse', False)
    sun_control = kwargs.get('sun_control', True)
    position_limit = int(kwargs.get('position_limit', 95))
    position_open = int(kwargs.get('position_open', 0))
    cloud_coverage_limit = int(kwargs.get('cloud_coverage_limit', 90))
    uv_index_limit = int(kwargs.get('uv_index_limit', 0))
    illumination_sensor = kwargs.get('illumination_sensor', None)
    illumination_threshold_open = int(kwargs.get('illumination_threshold_open', 200))
    illumination_threshold_close = int(kwargs.get('illumination_threshold_close', 200))
    window = Window(window_entity_id, reverse=reverse)
    if DEBUG:
        log.debug(f"{__name__}: using window entity: {window.entity_id} {window.friendly_name()}")
    window_fn = window.friendly_name()

    sun_state = state.getattr('sun.sun')
    azimuth = float(sun_state.get('azimuth') or -9999)
    elevation = float(sun_state.get('elevation') or -9999)

    weather_e = entity(WEATHER_ENTITY_ID)
    """
{'apparent_temperature': 21.1,
 'cloud_coverage': 90,
 'dew_point': 10.2,
 'humidity': 50,
 'precipitation_unit': 'mm',
 'pressure': 1016.5,
 'pressure_unit': 'hPa',
 'temperature': 20.9,
 'temperature_unit': '°C',
 'uv_index': 1,
 'visibility': 24.1,
 'visibility_unit': 'km',
 'wind_bearing': 180,
 'wind_gust_speed': 28.4,
 'wind_speed': 14.7,
 'wind_speed_unit': 'km/h'}
"""
    max_azimuth = AZIMUTH_HIGH
    min_azimuth = AZIMUTH_LOW

    if azimuth < min_azimuth or elevation > ELEVATION_HIGH:  # before noon
        if DEBUG:
            log.debug(f"""{__name__}: before noon:
            azimuth: {azimuth} < {min_azimuth}
            elevation: {elevation} > {ELEVATION_HIGH}
            Breaking.""")
        return

    # window_position = 100 - window_position
    # log.debug(f"window position: {window_position}")
    window_position_current = window.position()

    if illumination_sensor:
        i_sensor = entity(illumination_sensor)
        illumination = 1000
        try:
            illumination = int(i_sensor.state())
        except:
            pass

        if illumination <= illumination_threshold_open:
            slightly_less_open_position = max(window_position_current - 10, position_open)
            window.position_set(slightly_less_open_position)
            if DEBUG:
                log.debug(f"{__name__}: illumination is less than threshold: {illumination} <= {illumination_threshold_close}. Setting {slightly_less_open_position=}. {window_position_current=}")
            return


    cloud_coverage = int(weather_e.attrs().get('cloud_coverage', 0))
    if (elevation > 5
            and cloud_coverage_limit
            and cloud_coverage
            and cloud_coverage > cloud_coverage_limit):
        window.position_set(position_open)
        if DEBUG:
            log.debug(f"{__name__}: cloud_coverage is too high: {cloud_coverage}. Breaking.")
        return

    uv_index = int(weather_e.attrs().get('uv_index', 0))
    if (elevation > 5
            and uv_index_limit
            and uv_index
            and uv_index < uv_index_limit):
        window.position_set(position_open)
        if DEBUG:
            log.debug(f"{__name__}: uv_index is too low: {uv_index}. Breaking.")
        return

    # p = ha.datetime_p()
    # month = p.month
    # if 4 <= month <= 8:  # [april,august]
    steps = [
        # window_position_, step_high, step_low, step_force
        (50, ELEVATION_HIGH, 48, False),  # {step_high (or previous step_low)} >= {elevation} > {step_low}
        (60, None, 46, False),
        (70, None, 44, False),
        (80, None, 39, False),
        (90, None, 25, False),
        (100, None, 0.8, False),
        (60, None, 0.5, True),
        (position_open, None, ELEVATION_LOW, True),
    ]

    window_position = prev_high = position_open
    force = False
    if DEBUG:
        log.debug(f"Sun position: azimuth {azimuth}/{max_azimuth} elevation {elevation}/{ELEVATION_LOW}")

    if sun_control:
        if azimuth > max_azimuth or elevation < ELEVATION_LOW:
            window_position = position_open
            force = True
            if DEBUG:
                log.debug(f'''{min_azimuth} < azimuth {azimuth} > {max_azimuth}
                          {ELEVATION_LOW} > elevation {elevation} > {ELEVATION_HIGH}''')
        elif ((cloud_coverage_limit and cloud_coverage > cloud_coverage_limit)
              or (uv_index_limit and uv_index < uv_index_limit)):
            window_position = position_open
            force = True
            if DEBUG:
                log.debug(f'''cloud_coverage {cloud_coverage} > limit {cloud_coverage_limit}
                          uv_index: {uv_index} < limit {uv_index_limit}''')
        else:
            for window_position_, step_high, step_low, step_force in steps:
                step_high = step_high or prev_high
                prev_high = copy(step_high)
                if step_high >= elevation > step_low:
                    window_position = window_position_
                    force = step_force
                    window_position_current = window.position()
                    real_wanted_window_position = min(window_position, position_limit)
                    if window_position_current != real_wanted_window_position:  # print only if a change needs to be made
                        if DEBUG:
                            log.debug(f'''{window_fn}:
                                      step: {window_position_}, {step_high}, {step_low}, {step_force}
                                      {step_high} >= {elevation} > {step_low}: {window_position} {real_wanted_window_position} vs {window_position_current}''')
                    break

    window_position = min(window_position, position_limit)

    if window_position_current is not None and int_(window_position_current) == window_position:
        # log.debug(f"{__name__}: {window_fn} position is already: {window_position_current}. Breaking.")
        return

    if not force and window_position_current is not None and int_(window_position_current) > window_position:
        # log.debug(f"{__name__}: Won't close({window_position}) {window_fn} that is already "
        #           f"closed({window_position_current}).")
        return

    illumination = None
    if illumination_sensor is not None:
        i_sensor = entity(illumination_sensor)
        illumination = int_(i_sensor.state())
        if illumination <= illumination_threshold_close and int_(window_position_current) > window_position:
            window.position_set(position_open)
            if DEBUG:
                log.debug(f"{__name__}: illumination is less than threshold: {illumination} <= {illumination_threshold_close}.")
            return
        elif illumination >= illumination_threshold_close:
            window_position_current = window.position()
            slightly_less_open_position = max(window_position_current - 10, position_open)
            window.position_set(slightly_less_open_position)

    msg = f"""Azimuth: {azimuth} Elevation: {elevation}
{f' Illumination: {illumination}\n' if illumination_sensor is not None else ''}Setting {window_fn} position from {window_position_current} to {window_position}"""
    log.info(f"{__name__}:\n{msg}")

    # input_boolean_ = kwargs.get('input_boolean')
    # action_turn_off = f"input_boolean.turn_off(entity_id='{input_boolean_}')"
    # cb_turn_off = register_telegram_callback(action_turn_off)
    # action_open_cover = f"cover.set_cover_position(entity_id='{window.entity_id}', position={position_open})"
    # cb_open_cover = register_telegram_callback(action_open_cover)
    # inline = [
    #     [
    #         [f"Turn Off Automation", cb_turn_off],
    #         [f"Open {window_fn}", cb_open_cover],
    #     ],
    # ]
    # tools.telegram_message(msg, inline_keyboard=inline, disable_notification=True)
    tools.discord_message(msg, target=['1223990700266356847'])
    window.position_set(window_position)


def illumination_autowindow(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    window_entity_id = kwargs.get('window_entity_id')
    if not window_entity_id:
        log.info("Cannot _sun_autowindow: no window_entity_id")
        return

    reverse = kwargs.get('reverse', False)
    debug = kwargs.get('debug', DEBUG)
    position_close = int(kwargs.get('position_limit', 95))
    position_open = int(kwargs.get('position_open', 0))
    illumination_sensor = kwargs.get('illumination_sensor', None)
    illumination_threshold_open = int(kwargs.get('illumination_threshold_open', 200))
    illumination_threshold_close = int(kwargs.get('illumination_threshold_close', 200))
    window = Window(window_entity_id, reverse=reverse)
    if debug:
        log.debug(f"{__name__}: using window entity: {window.entity_id} {window.friendly_name()}")
    window_fn = window.friendly_name()

    window_position_current: int = window.position()
    if window_position_current is None:
        log.debug(f"{__name__}: window position is None. Breaking.")
        return

    force = False
    i_sensor = entity(illumination_sensor)
    try:
        illumination = int(i_sensor.state())
    except:
        log.debug(f"{__name__}: illumination is None. Breaking.")
        return

    if debug:
        log.debug(f"{__name__}: {window_fn} illumination: {illumination_threshold_open} <= {illumination} <= {illumination_threshold_close}")

    window_position = window_position_current
    if illumination <= illumination_threshold_open:
        window_position = window_position_current + 10 if not reverse else window_position_current - 10
        if debug:
            log.debug(f"{__name__}: illumination is less than open threshold: {illumination} <= {illumination_threshold_open}. Setting {window_position=}. {window_position_current=}")

    elif illumination >= illumination_threshold_close:
        window_position = window_position_current - 10 if not reverse else window_position_current + 10
        if debug:
            log.debug(f"{__name__}: illumination is more than open threshold: {illumination} <= {illumination_threshold_close}. Setting {window_position=}. {window_position_current=}")

    if reverse:
        window_position = min(window_position, position_close)
        window_position = max(window_position, position_open)
    else:
        window_position = max(window_position, position_close)
        window_position = min(window_position, position_open)

    if window_position_current == window_position:
        if debug:
            log.debug(f"{__name__}: {window_fn} position is already: {window_position_current}. Breaking.")
        return

    # if not force and window_position_current > window_position:
    #     if debug:
    #         log.debug(f"{__name__}: Won't close({window_position}) {window_fn} that is already closed({window_position_current}).")
    #     return

    msg = f"""Illumination: {illumination}.
Setting {window_fn} position from {window_position_current} to {window_position}"""
    log.info(f"{__name__}:\n{msg}")

    # input_boolean_ = kwargs.get('input_boolean')
    # action_turn_off = f"input_boolean.turn_off(entity_id='{input_boolean_}')"
    # cb_turn_off = register_telegram_callback(action_turn_off)
    # action_open_cover = f"cover.set_cover_position(entity_id='{window.entity_id}', position={position_open})"
    # cb_open_cover = register_telegram_callback(action_open_cover)
    # inline = [
    #     [
    #         [f"Turn Off Automation", cb_turn_off],
    #         [f"Open {window_fn}", cb_open_cover],
    #     ],
    # ]
    # tools.telegram_message(msg, inline_keyboard=inline, disable_notification=True)
    tools.discord_message(msg, target=['1223990700266356847'])
    window.position_set(window_position)
