from imports import *
from entities.climate import Climate
from entities.entity import Entity

DEBUG = False

DEFAULT_BOOST_TEMP_DIFFERENCE = 1.5
DEFAULT_TEMP_TOLERANCE_UP = 0.5
DEFAULT_TEMP_TOLERANCE_DOWN = 0.1
DEFAULT_TEMP_DIFFERENCE_FACTOR = 1.0
DEFAULT_HOLD = HOLD_1M
PRECISION = 0.1
MIN_TEMP = 18
MAX_TEMP = 32
PRESET_MODE_BOOST = 'boost'
PRESET_MODE_OFF = 'none'
HVAC_MODE_COOL = 'cool'
HVAC_MODE_HEAT = 'heat'
HVAC_MODE_FAN = 'fan_only'
HVAC_MODE_OFF = 'off'
FAN_MODE_AUTO = 'Auto'
FAN_MODES = ['Silence', '1', '2', '3', '4', '5']
DEFAULT_DISCORD_TARGET = '1111696430206287892'


# # EXAMPLE
# OFFICE_IB = 'input_boolean.office_auto_ac'
# OFFICE_WANTED_TEMP = 'input_number.office_wanted_temperature'
# OFFICE_ALLOWED_MODES = 'input_select.office_auto_ac_allowed_modes'
# OFFICE_TOLERANCE_UP = 0.1
# OFFICE_TOLERANCE_DOWN = 0.1
#
# OFFICE_KWARGS = dict(
#     ac_entity=OFFICE_AC,
#     cur_temp_entity=OFFICE_TEMPERATURE,
#     allowed_modes_selector=OFFICE_ALLOWED_MODES,
#     wanted_temperature_entity=OFFICE_WANTED_TEMP,
#     boost_trigger_difference=DEFAULT_BOOST_TEMP_DIFFERENCE,
#     tolerance_up=OFFICE_TOLERANCE_UP,
#     tolerance_down=OFFICE_TOLERANCE_DOWN,
#     change_temperature=True,
#     change_fan_speed=True,
#     fan_speed_limit=None,
#     allow_turning_off=2,  # index
# )
#
#
# @task_unique('auto_ac_office', kill_me=True)
# @state_trigger(
#     OFFICE_TEMPERATURE,
#     state_hold=DEFAULT_HOLD,
#     kwargs=OFFICE_KWARGS,
# )
# @state_trigger(
#     OFFICE_IB,
#     OFFICE_WANTED_TEMP,
#     OFFICE_ALLOWED_MODES,
#     state_hold=2,
#     kwargs=OFFICE_KWARGS,
# )
# @conditional(
#     entity_on(OFFICE_IB),
#     entity_exists(OFFICE_AC),
#     entity_exists(OFFICE_TEMPERATURE),
#     entity_exists(OFFICE_WANTED_TEMP),
#     entity_exists(OFFICE_ALLOWED_MODES),
# )
# def auto_ac_office(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
#     ib = entity(OFFICE_IB)
#     if ib.state() != 'on':
#         return
#
#     return auto_ac(trigger_type=trigger_type, var_name=var_name, value=value, old_value=old_value,
#                    context=context, **kwargs)


def turn_off(ac_entity, allow_turning_off=True, ac_action_wait=4):
    if not isinstance(ac_entity, Climate):
        if isinstance(ac_entity, str):
            ac_entity = Climate(ac_entity)
        elif isinstance(ac_entity, Entity):
            ac_entity = Climate(ac_entity.entity_id)

    if allow_turning_off is True:
        on = ac_entity.is_on()
        if on:
            ac_entity.turn_off()
            task.sleep(ac_action_wait)
        on = ac_entity.is_on()
        if on:
            ac_entity.turn_off()
            task.sleep(ac_action_wait)
    else:
        hvac_mode = ac_entity.hvac_mode()
        if hvac_mode != HVAC_MODE_FAN:
            ac_entity.set_hvac_mode(HVAC_MODE_FAN)
            task.sleep(ac_action_wait)
        preset_mode = ac_entity.preset_mode()
        if preset_mode != PRESET_MODE_OFF:
            ac_entity.set_preset_mode(PRESET_MODE_OFF)
            task.sleep(ac_action_wait)

        try:
            fan_mode = FAN_MODES[allow_turning_off]
        except:
            fan_mode = FAN_MODES[0]

        ac_fan_mode = ac_entity.fan_mode()
        if ac_fan_mode != fan_mode:
            ac_entity.set_fan_mode(fan_mode)
            task.sleep(ac_action_wait)


def auto_ac(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    #     'entity_id': 'climate.ac_office',
    #     'state': 'cool',
    #     'attributes': {
    #         'hvac_modes': [
    #             <HVACMode.FAN_ONLY: 'fan_only'>,
    #             <HVACMode.DRY: 'dry'>,
    #             <HVACMode.COOL: 'cool'>,
    #             <HVACMode.HEAT: 'heat'>,
    #             <HVACMode.HEAT_COOL: 'heat_cool'>,
    #             <HVACMode.OFF: 'off'>
    #         ],
    #         'min_temp': 7,
    #         'max_temp': 35,
    #         'target_temp_step': 1,
    #         'fan_modes': ['Auto', 'Silence', '1', '2', '3', '4', '5'],
    #         'preset_modes': ['none', 'away', 'eco', 'boost'],
    #         'swing_modes': ['Off', 'Vertical', 'Horizontal', '3D'],
    #         'current_temperature': 24.0,
    #         'temperature': 24.0,
    #         'fan_mode': 'Silence',
    #         'hvac_action': <HVACAction.COOLING: 'cooling'>,
    #         'preset_mode': 'none',
    #         'swing_mode': 'Off',
    #         'friendly_name': 'OfficeAC',
    #         'supported_features': <ClimateEntityFeature.SWING_MODE|PRESET_MODE|FAN_MODE|TARGET_TEMPERATURE: 57>},
    #         'last_changed': '2023-05-23T16:32:31.787600+00:00',
    #         'last_updated': '2023-05-23T16:32:31.787600+00:00',
    wanted_temp_entity_id = kwargs.get('wanted_temperature_entity')
    ac_entity_id = kwargs.get('ac_entity')
    assert ac_entity_id, f"ac_entity_id: {ac_entity_id}, kwargs: {kwargs}"

    ac_entity = Climate(ac_entity_id)
    ac_precision = float(int(ac_entity.state('target_temp_step', 1)))

    tolerance_up = float(kwargs.get('tolerance_up', DEFAULT_TEMP_TOLERANCE_UP))
    tolerance_down = kwargs.get('tolerance_down', DEFAULT_TEMP_TOLERANCE_DOWN)
    temp_difference_factor = float(kwargs.get('temp_difference_factor', DEFAULT_TEMP_DIFFERENCE_FACTOR))

    cur_temp_entity_id = kwargs.get('cur_temp_entity')
    change_temperature = kwargs.get('change_temperature', True)
    change_fan_speed = kwargs.get('change_fan_speed', True)
    boost_temp_difference = float(kwargs.get('boost_trigger_difference', DEFAULT_BOOST_TEMP_DIFFERENCE))
    allowed_modes_selector = kwargs.get('allowed_modes_selector', None)
    fan_speed_limit = kwargs.get('fan_speed_limit', None)
    fan_speed_limit_min = kwargs.get('fan_speed_limit_min', None)
    allow_turning_off = kwargs.get('allow_turning_off', True)
    discord_target = kwargs.get('discord_target', DEFAULT_DISCORD_TARGET)
    debug = kwargs.get('debug', DEBUG)

    cur_temp_entity = entity(cur_temp_entity_id)
    cur_temp = round(float(cur_temp_entity.state()), 1)
    cur_temp_friendly_name = cur_temp_entity.friendly_name()

    # try:
    #     ac_hvac_mode = ac_entity.hvac_mode()
    #     ac_preset_mode = ac_entity.preset_mode()
    #     ac_fan_speed = ac_entity.fan_mode()
    # except Exception as e:
    #     log.debug(f"{ac_entity_id} {type(ac_entity)} {ac_entity} exception: {type(e)} {str(e)}")
    #     return

    ac_hvac_mode = ac_entity.state()
    ac_preset_mode = ac_entity.preset_mode()
    ac_fan_speed = ac_entity.fan_mode()

    ac_temperature = float(ac_entity.state('temperature', cur_temp) or cur_temp)
    ac_friendly_name = ac_entity.friendly_name()
    ac_action_wait = 3
    ac_inside_temp = float(ac_entity.state('current_temperature', cur_temp) or cur_temp)

    msgs = DiscordMsgBucket(name=f"{__name__} for {ac_friendly_name}", target=discord_target)

    wanted_temp_entity = entity(wanted_temp_entity_id)
    wanted_temp_entity_friendly_name = wanted_temp_entity.friendly_name()
    wanted_temp = float(wanted_temp_entity.state())

    temp_low_bar = wanted_temp - tolerance_down
    msgs.add(f'low bar: {wanted_temp}-{tolerance_down}={temp_low_bar}')
    temp_high_bar = wanted_temp + tolerance_up
    msgs.add(f'high bar: {wanted_temp}+{tolerance_down}={temp_high_bar}')

    temp_difference = round(float(cur_temp - wanted_temp), 1)
    # log.debug(f"temp_difference = round(float(cur_temp {cur_temp} - wanted_temp {wanted_temp}), 1) = {temp_difference}")
    temp_difference_abs = abs(temp_difference)
    # log.debug(f"temp_difference_abs={temp_difference_abs}")

    allowed_modes = [HVAC_MODE_COOL, HVAC_MODE_HEAT]
    if allowed_modes_selector:
        allowed_modes_selector_entity = entity(allowed_modes_selector)
        allowed_mode = allowed_modes_selector_entity.state()
        allowed_modes = [_ for _ in allowed_modes if _ in allowed_mode.lower()]
    allowed_modes.append(HVAC_MODE_FAN)
    allowed_modes.append(HVAC_MODE_OFF)

    wanted_state = HVAC_MODE_OFF
    preset_target = PRESET_MODE_OFF

    if debug:
        log.debug(f"{temp_high_bar=} {cur_temp=} {wanted_temp=} {temp_low_bar=}")

    if cur_temp > temp_high_bar:
        msgs.add(f'{cur_temp} > ↑{temp_high_bar}')
        wanted_state = HVAC_MODE_COOL
        if debug:
            log.debug(f"{cur_temp=} > {temp_high_bar=}: {wanted_state=}")
    elif cur_temp < temp_low_bar:  # got it
        msgs.add(f'{cur_temp} < ↓{temp_low_bar}')
        wanted_state = HVAC_MODE_HEAT
        if debug:
            log.debug(f"{cur_temp=} < {temp_low_bar=}: {wanted_state=}")
    elif cur_temp == wanted_temp:
        if debug:
            log.debug(f"{cur_temp=} == {wanted_temp=}")
        msgs.add(f'{ac_friendly_name} temperature reached: {wanted_state}. Turning off.')
        msgs.send()
        turn_off(ac_entity, allow_turning_off, ac_action_wait)
        return

    else:
        wanted_state = ac_hvac_mode
        msgs.add(f'{temp_high_bar} ↑ {cur_temp} ↓ {temp_low_bar}')

    if wanted_state not in allowed_modes:
        msgs.add(f'{ac_friendly_name} wanted_state unallowed: {wanted_state}. Turning off.')
        msgs.send()
        turn_off(ac_entity, allow_turning_off, ac_action_wait)
        return
    elif ac_hvac_mode != wanted_state:
        msgs.add(f"wanted_state: {wanted_state}")

    if ac_hvac_mode != HVAC_MODE_OFF and wanted_state == HVAC_MODE_OFF:
        if debug:
            log.debug(f"{ac_friendly_name} wanted_state off. Turning off.")
        msgs.send()
        turn_off(ac_entity, allow_turning_off, ac_action_wait)
        return
    elif ac_hvac_mode == HVAC_MODE_OFF and wanted_state == HVAC_MODE_OFF:
        if debug:
            log.debug(f"{ac_friendly_name} ac_hvac_mode == wanted_state == {HVAC_MODE_OFF}")
        return

    if ac_hvac_mode != HVAC_MODE_OFF and ac_hvac_mode not in allowed_modes:
        msgs.add(f'{ac_friendly_name} current state unallowed: {ac_hvac_mode}. Turning off.')
        msgs.send()
        turn_off(ac_entity, allow_turning_off, ac_action_wait)
        return

    # AC thinks it's 26 = but it's 24.  wanted 22.    proportion (26/24)*22
    target_temperature = round((ac_inside_temp/cur_temp) * wanted_temp, 2)
    msgs.add(f'{ac_friendly_name} target_temperature raw: {target_temperature}')
    target_temperature = round(target_temperature, 2)  # just for visual clarity
    msgs.add(f'target_temperature round: {target_temperature}')

    msgs.add(f'temp_difference_factor: {temp_difference_factor}')

    if wanted_temp > cur_temp:  # heating
        # `+ ac_precision + tolerance_up` makes it more agressive
        # can be just `+ tolerance_up` or just `+ ac_precision`
        target_temperature = target_temperature + ac_precision + tolerance_up
        target_temperature *= temp_difference_factor
        target_temperature = tools.round_up(target_temperature, ac_precision)
    elif wanted_temp < cur_temp:  # cooling
        target_temperature = target_temperature - ac_precision - tolerance_down
        target_temperature /= temp_difference_factor
        target_temperature = tools.round_down(target_temperature, ac_precision)
    else:
        target_temperature = ac_temperature

    msgs.add(f'target_temperature rounded: {target_temperature}')

    target_temperature = max(target_temperature, MIN_TEMP)
    target_temperature = min(target_temperature, MAX_TEMP)

    msgs.add(f'target_temperature minmaxed: {target_temperature} vs ac_inside {ac_inside_temp}')

    try:
        index_try = FAN_MODES.index(ac_fan_speed)
    except:
        index_try = 'Unknown'

    msgs_init = [
        f":leaves: {__name__} for {ac_friendly_name}:",
        f"🌡️ {cur_temp_friendly_name}: {cur_temp}",
        f"🎯 {wanted_temp_entity_friendly_name}: {wanted_temp}",
        f'temp_difference: {temp_difference}',
        f"hvac_mode: {ac_hvac_mode}",
        f"allowed_modes: {allowed_modes}",
        f"preset_mode: {ac_preset_mode}",
        f"🌬️fan_speed: {ac_fan_speed}: {index_try}/{len(FAN_MODES)}",
    ]

    if ac_hvac_mode != wanted_state and wanted_state in allowed_modes:
        msgs.add(f'Setting HVAC Mode {ac_hvac_mode} to {wanted_state}')
        ac_entity.set_hvac_mode(wanted_state)
        task.sleep(ac_action_wait)

    if change_fan_speed:  # and temp_difference_ok
        wanted_fan_speed = abs(float(len(FAN_MODES)) * (temp_difference or 0.1) / float(boost_temp_difference or 2))
        wanted_fan_speed -= 1  # indexes from 0
        if debug:
            log.debug(f"before mod: {wanted_fan_speed}")
        if (wanted_fan_speed_div := wanted_fan_speed % 1.0) >= 0.5:
            wanted_fan_speed -= wanted_fan_speed_div
            wanted_fan_speed += 1
            if debug:
                log.debug(f"after mod: {wanted_fan_speed}")

        wanted_fan_speed = int(round(wanted_fan_speed, 0))
        if debug:
            log.debug(f"after int: {wanted_fan_speed}")

        if fan_speed_limit is not None:
            wanted_fan_speed = min(wanted_fan_speed, int(fan_speed_limit))
            if debug:
                log.debug(f"after fan_speed_limit: {wanted_fan_speed}")

        if fan_speed_limit_min is not None:
            wanted_fan_speed = max(wanted_fan_speed, int(fan_speed_limit_min))
            if debug:
                log.debug(f"after fan_speed_limit_min: {wanted_fan_speed}")

        if wanted_fan_speed > len(FAN_MODES) - 1:
            preset_target = PRESET_MODE_BOOST
            if debug:
                log.debug(f"too much boost: {wanted_fan_speed} > {len(FAN_MODES) - 1}")
        else:
            wanted_fan_speed = max(min(wanted_fan_speed, len(FAN_MODES) - 1), 0)
            if DEBUG:
                log.debug(f"after max: {wanted_fan_speed}")
                log.debug(f"""{ac_friendly_name}
                          float(len(FAN_MODES)) * (temp_difference or 0.1) / float(boost_temp_difference):
                          {float(len(FAN_MODES))} * {(temp_difference or 0.1)} / {float(boost_temp_difference)}
                          wanted_fan_speed: {wanted_fan_speed}/{len(FAN_MODES)}""")

            try:
                wanted_fan_speed = FAN_MODES[wanted_fan_speed]
            except Exception as e:
                tools.telegram_message_alert_ha_private(
                    f"error wanted_fan_speed: {wanted_fan_speed} of {FAN_MODES} {type(e)} {e}")
                wanted_fan_speed = FAN_MODES[0]

            if ac_fan_speed != wanted_fan_speed:
                msgs.add(f'Setting fan speed {ac_fan_speed} to {wanted_fan_speed}/{len(FAN_MODES)}')
                ac_entity.set_fan_mode(wanted_fan_speed)
                task.sleep(ac_action_wait)

    if ac_preset_mode != preset_target:
        msgs.add(f'Setting preset mode {ac_preset_mode} to {preset_target}')
        ac_entity.set_preset_mode(preset_target)
        task.sleep(ac_action_wait)

    if change_temperature and ac_temperature != target_temperature and temp_difference_abs > 0:
        msgs.add(f'Setting {ac_friendly_name} temperature {ac_temperature} to {target_temperature}')
        ac_entity.set_temperature(hvac_mode=wanted_state, temperature=target_temperature)
                                  # target_temp_high=target_temperature_max, target_temp_low=target_temperature_min)
        task.sleep(ac_action_wait)
    elif ac_temperature == target_temperature:
        msgs.add(f'{ac_friendly_name} temperature already set to {target_temperature}')

    if msgs.msgs:
        msgs.msgs = msgs_init + msgs.msgs
        msgs.send()
    else:
        if debug:
            log.debug(f"{__name__}: nothing to do for {ac_friendly_name}")
