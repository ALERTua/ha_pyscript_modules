from imports import *


DEFAULT_TOLERANCE_DOWN = 0.5
DEFAULT_TOLERANCE_UP = 0.3
DEFAULT_MIN_TEMP = 18
DEFAULT_MAX_TEMP = 30
MAX_TEMP = 29
DEFAULT_NOTIFICATION_CHANNEL = '1194571076949262408'
DEFAULT_VALVE_HOLD = HOLD_3M
DEFAULT_VALVE_HOLD_FALSE = HOLD_3M
DEFAULT_TEMP_FACTOR = 1.0
OVERTEMP_PROTECTION = 3

# # EXAMPLE
# DEFAULT_VALVE_HOLD = HOLD_3M
# DEFAULT_VALVE_HOLD_FALSE = HOLD_3M
# DEFAULT_TEMP_FACTOR = 1.0
#
#
# OFFICE_VALVE_IB = 'input_boolean.office_auto_valve'
# OFFICE_VALVE_KWARGS = dict(
#     valve_entity_id=OFFICE_VALVE,
#     cur_temp_entity=OFFICE_TEMPERATURE,
#     wanted_temperature_entity=OFFICE_WANTED_TEMP,
#     temp_diff_factor=DEFAULT_TEMP_FACTOR,
#     position_entity_id=OFFICE_VALVE_POSITION,
#     allow_turning_off=True,
#     hvac_mode_on='auto',
#     notification_channel='1198228933288661043',
# )
#
#
# @task_unique('auto_valve_office_f', kill_me=True)
# @state_trigger(
#     OFFICE_TEMPERATURE,
#     # state_hold=DEFAULT_VALVE_HOLD,
#     state_hold_false=DEFAULT_VALVE_HOLD_FALSE,
#     kwargs=OFFICE_VALVE_KWARGS,
# )
# @state_trigger(
#     OFFICE_VALVE_IB,
#     OFFICE_WANTED_TEMP,
#     state_hold=2,
#     kwargs=OFFICE_VALVE_KWARGS,
# )
# @conditional(
#     entity_on(OFFICE_VALVE_IB),
#     entity_exists(OFFICE_VALVE),
#     entity_exists(OFFICE_TEMPERATURE),
# )
# def auto_valve_office_f(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
#     ib = entity(OFFICE_VALVE_IB)
#     if ib.state() != 'on':
#         return
#
#     return auto_valve(trigger_type=trigger_type, var_name=var_name, value=value, old_value=old_value, context=context,
#                       **kwargs)


def auto_valve(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    wanted_temp_entity_id = kwargs.get('wanted_temperature_entity') or None
    valve_entity_id = kwargs.get('valve_entity_id') or None
    assert valve_entity_id, f"valve_entity_id: {valve_entity_id}, kwargs: {kwargs}"
    real_temp_entity_id = kwargs.get('cur_temp_entity') or None
    position_entity_id = kwargs.get('position_entity_id') or None
    allow_turning_off = kwargs.get('allow_turning_off', False) or False
    temp_diff_factor = kwargs.get('temp_diff_factor', DEFAULT_TEMP_FACTOR) or DEFAULT_TEMP_FACTOR
    tolerance_down = kwargs.get('tolerance_down', DEFAULT_TOLERANCE_DOWN)
    tolerance_up = kwargs.get('tolerance_up', DEFAULT_TOLERANCE_UP)
    hvac_mode_on = kwargs.get('hvac_mode_on', None)
    notification_channel = str(kwargs.get('notification_channel', DEFAULT_NOTIFICATION_CHANNEL))

    real_temp_entity = entity(real_temp_entity_id)
    real_temp = round(float(real_temp_entity.state()), 1)
    real_temp_friendly_name = real_temp_entity.friendly_name()

    valve_entity = entity(valve_entity_id)
    valve_state = valve_entity.state()
    if not allow_turning_off and valve_state == 'off':
        log.debug("valve_state == 'off'. Breaking")
        return

    valve_min_temp = valve_entity.attrs().get('min_temp', DEFAULT_MIN_TEMP)
    valve_max_temp = valve_entity.attrs().get('max_temp', DEFAULT_MAX_TEMP)
    valve_preset_mode = valve_entity.attrs().get('preset_mode')
    valve_target_temp = round(float(valve_entity.attrs().get('temperature', real_temp) or real_temp), 1)
    valve_friendly_name = valve_entity.friendly_name()
    valve_cur_temp = float(valve_entity.attrs().get('current_temperature', real_temp) or real_temp)
    try:
        valve_position = int(state.get(position_entity_id))
    except:
        valve_position = None

    vlv = f'{valve_friendly_name}({valve_position})' if valve_position is not None else valve_friendly_name
    wanted_temp_entity = entity(wanted_temp_entity_id)
    wanted_temp_entity_friendly_name = wanted_temp_entity.friendly_name()
    wanted_temp = round(float(wanted_temp_entity.state()), 1)

    msgs = DiscordMsgBucket(name=f"{__name__} for {vlv}", target=notification_channel)
    msgs_init = [
        f":hotsprings:{__name__} for {vlv}: {valve_state} {valve_preset_mode}",
        f"{real_temp_friendly_name} 🌡️{real_temp} vs {wanted_temp}🎯 {wanted_temp_entity_friendly_name}",
        f"current temperature: {valve_cur_temp}",
    ]
    msgs.msgs = msgs_init

    temp_diff = round(float(real_temp - wanted_temp), 1)
    msgs.add(f'temp_diff: {temp_diff}')
    if temp_diff_factor != 1.0:
        temp_diff *= temp_diff_factor
        msgs.add(f'temp_diff after factor: {temp_diff}')

    # log.debug(f"temp_difference = round(float(cur_temp {cur_temp} - wanted_temp {wanted_temp}), 1) = {temp_difference}")
    temp_difference_abs = abs(temp_diff)
    # log.debug(f"temp_difference_abs={temp_difference_abs}")

    if real_temp >= wanted_temp + tolerance_up:  # off
        msg = f':white_check_mark: real({real_temp}) >= wanted({wanted_temp}) + tolerance_up({tolerance_up})'
        msgs.add(msg)
        if valve_state != 'off':
            if valve_target_temp != wanted_temp:
                msg = f"{vlv} {wanted_temp} reached. Setting Valve Temperature {valve_target_temp} to {wanted_temp}."
                msgs.add(msg)
                valve_entity.set_temperature(temperature=wanted_temp, hvac_mode=valve_state)
            if allow_turning_off:
                if valve_position is None or valve_position > 15:
                    msgs.add(f'position: {valve_position}. Turning off')
                    valve_entity.turn_off()
            msgs.send()
        return

    elif real_temp >= wanted_temp:
        msg = f'{vlv} real {real_temp} >= {wanted_temp} wanted, but not above tolerance {tolerance_up}. Breaking'
        # log.debug(msg)
        # msgs.add(msg)
        # msgs.send()
        return

    elif real_temp < wanted_temp - tolerance_down:  # on
        msgs.add(f'real {real_temp} < {wanted_temp} wanted')
        if allow_turning_off and valve_state == 'off':
            msgs.add(f'Turning on')
            valve_entity.turn_on()
            task.sleep(3)
            if hvac_mode_on:
                valve_entity.set_hvac_mode(hvac_mode_on)
                task.sleep(5)
    elif real_temp <= wanted_temp:
        msg = f'{vlv} real {real_temp} <= {wanted_temp} wanted, but not below tolerance {tolerance_down}. Breaking'
        log.debug(msg)
        # msgs.add(msg)
        # msgs.send()
        return
    elif valve_cur_temp >= wanted_temp + tolerance_up + OVERTEMP_PROTECTION:  # off?
        msg = (f':white_check_mark:  {vlv} current temp({valve_cur_temp}) >= wanted({wanted_temp}) + '
               f'tolerance_up({tolerance_up}) + overtemp_protection({OVERTEMP_PROTECTION})')
        msgs.add(msg)
        if valve_target_temp != wanted_temp:
            msg = (f"{vlv} temp({valve_cur_temp}) >= wanted_temp({wanted_temp}) + tolerance_up({tolerance_up}) "
                   f"+ overtemp_protection({OVERTEMP_PROTECTION})")
            msgs.add(msg)
            valve_entity.set_temperature(temperature=wanted_temp, hvac_mode=valve_state)
        if allow_turning_off and valve_state != 'off':
            if valve_position is None or valve_position > 15:
                msgs.add(f'position: {valve_position}. Turning off')
                valve_entity.turn_off()
        msgs.send()
        return
    else:
        msgs.add(f'{vlv} real {real_temp} <> {wanted_temp} wanted')

    # log.debug(f"{vlv} valve_min_temp: {valve_min_temp}")
    # log.debug(f"{vlv} valve_max_temp: {valve_max_temp}")
    target_temp = round(valve_cur_temp - temp_diff, 1)
    # log.debug(f"{vlv} target_temp 1: {target_temp}")
    target_temp = max(target_temp, valve_min_temp)
    # log.debug(f"{vlv} target_temp 2: {target_temp}")
    target_temp = min(target_temp, valve_max_temp, MAX_TEMP)
    # log.debug(f"{vlv} target_temp 3: {target_temp}")

    valve_state = valve_entity.state()
    # log.debug(f"{vlv} valve_state: {valve_state}")
    if valve_target_temp == target_temp:  # todo: ?!
    #     if valve_target_temp != wanted_temp:
    #         msg = f"{vlv} No Temperature difference. Setting Valve Temperature to {wanted_temp}."
    #         log.debug(msg)
    #         msgs.add(msg)
    #         valve_entity.set_temperature(temperature=wanted_temp, hvac_mode=valve_state)
    #         msgs.send()
        return

    if ((temp_diff > 0 and temp_difference_abs < tolerance_up)
            or (temp_diff < 0 and temp_difference_abs < tolerance_down)):
        msg = f"{vlv} Temperature difference too low. Setting Valve Temperature to {wanted_temp}."
        msgs.add(msg)
        valve_entity.set_temperature(temperature=wanted_temp, hvac_mode=valve_state)
    else:
        msgs.add(f'{vlv} Setting temperature {valve_target_temp} to {target_temp}')
        valve_entity.set_temperature(temperature=target_temp, hvac_mode=valve_state)

    msgs.send()
