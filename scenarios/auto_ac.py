from imports import *
from entities.climate import Climate
from entities.entity import Entity

DEBUG = False

DEFAULT_BOOST_TEMP_DIFFERENCE = 1.5
DEFAULT_TEMP_TOLERANCE_UP = 0.5
DEFAULT_TEMP_TOLERANCE_DOWN = 0.1
DEFAULT_TEMP_DIFFERENCE_FACTOR = 1.0  # 1.0 = aim at target; >1 overshoots ∝ deviation
DEFAULT_MIN_MARGIN_STEPS = 2.0  # min setpoint gap past wanted, in AC steps (min_margin = this * step)
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
#     mode_selector=OFFICE_ALLOWED_MODES,
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


def auto_ac(
    trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs
):
    """Drive one AC toward wanted_temp and stop at it, so the room oscillates between
    wanted and one tolerance bar. In cool it runs while the room is above wanted and
    re-engages only after the room drifts up past wanted + tolerance_up (heat mirrors
    this with wanted - tolerance_down). Fan speed scales with the deviation from wanted.

    Notes:
    - Boost is intentionally gated by `change_fan_speed`: boost is the top of the
      fan-speed ramp, so if fan-speed control is off, boost is off too. A set
      `fan_speed_limit` likewise suppresses boost — the limit is a declared ceiling.
    - `FAN_MODES` intentionally excludes 'Auto': the AC's Auto mode regulates off its
      own (inaccurate) internal sensor, so we always pick an explicit numeric speed.
    - `temp_difference_factor` controls setpoint aggressiveness. The target sent to the AC
      is pushed past `wanted` by `(temp_difference_factor - 1) * (cur_temp - wanted)`, so a
      larger current deviation pushes the setpoint further and the AC keeps working hard
      instead of easing off as it nears `wanted` (faster pull-in). The push shrinks to 0 as
      the room reaches `wanted`, so it self-corrects: `1.0` aims exactly at `wanted`, `1.5`
      overshoots by half the current deviation, `2.0` mirrors it. The push is floored by
      `min_margin` (below), so near `wanted` it eases toward — but never above — that floor.
      Nuances: it sets how hard we approach `wanted`, NOT the swing amplitude (that is the
      on/off band). Fan speed / boost is the other deviation-driven lever, and it dominates
      "intensity" on simple on/off ACs (there a lower setpoint mostly changes run time /
      overshoot, not compressor effort).
    - `min_margin_steps` floors how far past `wanted` the setpoint sits while running, as a
      multiple of the AC's temperature step (`min_margin = min_margin_steps * target_temp_step`).
      It guarantees a real gap so the compressor actually runs and the room reaches `wanted`
      instead of stalling short; the script stops the AC at `wanted`. Bigger = reaches the
      target more reliably but may overshoot slightly past it. Coarser ACs (bigger step) get
      a wider gap automatically.
    """
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
    ac_precision = (
            kwargs.get('target_temp_step', None)
            or float_(ac_entity.state('target_temp_step', PRECISION), default=PRECISION)
            or PRECISION
    )

    tolerance_up = float(kwargs.get('tolerance_up', DEFAULT_TEMP_TOLERANCE_UP))
    tolerance_down = float(kwargs.get('tolerance_down', DEFAULT_TEMP_TOLERANCE_DOWN))
    temp_difference_factor = float(
        kwargs.get('temp_difference_factor', DEFAULT_TEMP_DIFFERENCE_FACTOR)
    )
    min_margin_steps = float(kwargs.get('min_margin_steps', DEFAULT_MIN_MARGIN_STEPS))

    cur_temp_entity_id = kwargs.get('cur_temp_entity')
    change_temperature = kwargs.get('change_temperature', True)
    change_fan_speed = kwargs.get('change_fan_speed', True)
    boost_temp_difference = float(
        kwargs.get('boost_trigger_difference', DEFAULT_BOOST_TEMP_DIFFERENCE)
    )
    mode_selector = kwargs.get('mode_selector', None)
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

    msgs = DiscordMsgBucket(
        name=f"{__name__} for {ac_friendly_name}", target=discord_target
    )
    msgs.add(f"{ac_precision=}")
    wanted_temp_entity = entity(wanted_temp_entity_id)
    wanted_temp_entity_friendly_name = wanted_temp_entity.friendly_name()
    wanted_temp = float(wanted_temp_entity.state())

    temp_low_bar = round(wanted_temp - tolerance_down, 2)
    msgs.add(f'low bar: {wanted_temp}-{tolerance_down}={temp_low_bar}')
    temp_high_bar = round(wanted_temp + tolerance_up, 2)
    msgs.add(f'high bar: {wanted_temp}+{tolerance_up}={temp_high_bar}')

    temp_difference = round(float(cur_temp - wanted_temp), 1)
    # log.debug(f"temp_difference = round(float(cur_temp {cur_temp} - wanted_temp {wanted_temp}), 1) = {temp_difference}")
    temp_difference_abs = abs(temp_difference)
    # log.debug(f"temp_difference_abs={temp_difference_abs}")

    # Single direction: this AC only cools OR only heats (no combined mode).
    mode = HVAC_MODE_COOL
    if mode_selector:
        selected = (entity(mode_selector).state() or '').lower()
        mode = HVAC_MODE_HEAT if HVAC_MODE_HEAT in selected else HVAC_MODE_COOL

    preset_target = PRESET_MODE_OFF
    running = ac_hvac_mode == mode  # is the AC currently driving in its direction

    if debug:
        log.debug(f"{temp_high_bar=} {cur_temp=} {wanted_temp=} {temp_low_bar=} {mode=} {running=}")

    if mode == HVAC_MODE_COOL:
        if cur_temp <= wanted_temp:        # reached target -> stop (never cool below wanted)
            want_on = False
        elif cur_temp > temp_high_bar:     # went beyond the tolerance bar -> cool again
            want_on = True
        else:                              # between wanted and high_bar -> keep current state
            want_on = running
    else:  # HVAC_MODE_HEAT
        if cur_temp >= wanted_temp:        # reached target -> stop (never heat above wanted)
            want_on = False
        elif cur_temp < temp_low_bar:      # went beyond the tolerance bar -> heat again
            want_on = True
        else:
            want_on = running

    msgs.add(f'{temp_low_bar} ↓ {cur_temp} ↑ {temp_high_bar} | mode={mode} want_on={want_on}')

    if not want_on:
        if running:  # only stop if we were actually driving; don't fight a manual off
            msgs.add(f'{ac_friendly_name} reached wanted. Turning off.')
            msgs.send()
            turn_off(ac_entity, allow_turning_off, ac_action_wait)
        return

    wanted_state = mode


    # Setpoint = proportional push toward `wanted` (temp_difference_factor on the
    # deviation) floored by a minimum drive margin, so the AC always keeps a real gap to
    # work on and doesn't stall short of `wanted`; the script itself stops it at `wanted`.
    #   prop = wanted - (temp_difference_factor - 1) * (cur_temp - wanted)
    #   cool: room_aim = min(prop, wanted - min_margin);  heat: max(prop, wanted + min_margin)
    #   ac setpoint = room_aim + (ac_inside_temp - cur_temp)   (sensor-offset compensation)
    # min_margin = min_margin_steps * ac_precision (coarser ACs need a wider gap to run).
    min_margin = ac_precision * min_margin_steps
    sensor_offset = round(ac_inside_temp - cur_temp, 2)
    prop_room = wanted_temp - (temp_difference_factor - 1) * temp_difference
    if mode == HVAC_MODE_HEAT:
        room_aim = max(prop_room, wanted_temp + min_margin)
        target_temperature = tools.round_up(room_aim + sensor_offset, ac_precision, round_result=2)
    else:  # cool
        room_aim = min(prop_room, wanted_temp - min_margin)
        target_temperature = tools.round_down(room_aim + sensor_offset, ac_precision, round_result=2)
    msgs.add(
        f'{ac_friendly_name} target: {target_temperature} | room_aim={round(room_aim, 2)} {temp_difference_factor=} {temp_difference=} {min_margin=} {sensor_offset=}'
    )

    msgs.add(f'target_temperature rounded: {target_temperature}')

    target_temperature = max(target_temperature, MIN_TEMP)
    target_temperature = min(target_temperature, MAX_TEMP)

    msgs.add(
        f'target_temperature minmaxed: {target_temperature} vs ac_inside {ac_inside_temp}'
    )

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
        f"mode: {mode}",
        f"preset_mode: {ac_preset_mode}",
        f"🌬️fan_speed: {ac_fan_speed}: {index_try}/{len(FAN_MODES)}",
    ]

    if ac_hvac_mode != wanted_state:
        msgs.add(f'Setting HVAC Mode {ac_hvac_mode} to {wanted_state}')
        ac_entity.set_hvac_mode(wanted_state)
        task.sleep(ac_action_wait)

    if change_fan_speed:  # and temp_difference_ok
        wanted_fan_speed = abs(
            float(len(FAN_MODES))
            * (temp_difference or 0.1)
            / float(boost_temp_difference or 2)
        )
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

        # Boost is decided on the physical deviation, not on the derived fan index
        # (the `-1` + rounding on the index shifted the real trigger ~8% past boost).
        # A set fan_speed_limit is a declared ceiling, so it overrides (suppresses) boost.
        boost_allowed = fan_speed_limit is None
        if boost_allowed and temp_difference_abs > boost_temp_difference:
            preset_target = PRESET_MODE_BOOST
            if debug:
                log.debug(f"boost: {temp_difference_abs} > {boost_temp_difference}")
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
                    f"error wanted_fan_speed: {wanted_fan_speed} of {FAN_MODES} {type(e)} {e}"
                )
                wanted_fan_speed = FAN_MODES[0]

            if ac_fan_speed != wanted_fan_speed:
                msgs.add(
                    f'Setting fan speed {ac_fan_speed} to {wanted_fan_speed}/{len(FAN_MODES)}'
                )
                ac_entity.set_fan_mode(wanted_fan_speed)
                task.sleep(ac_action_wait)

    if ac_preset_mode != preset_target:
        msgs.add(f'Setting preset mode {ac_preset_mode} to {preset_target}')
        ac_entity.set_preset_mode(preset_target)
        task.sleep(ac_action_wait)

    if (
        change_temperature
        and ac_temperature != target_temperature
        # and temp_difference_abs > ac_precision
    ):
        msgs.add(f'Setting {ac_friendly_name} temperature {ac_temperature} to {target_temperature}')
        ac_entity.set_temperature(hvac_mode=wanted_state, temperature=target_temperature)
        task.sleep(ac_action_wait)
    elif ac_temperature == target_temperature:
        msgs.add(f'{ac_friendly_name} temperature already set to {target_temperature}')

    if msgs.msgs:
        msgs.msgs = msgs_init + msgs.msgs
        msgs.send()
    else:
        if debug:
            log.debug(f"{__name__}: nothing to do for {ac_friendly_name}")
