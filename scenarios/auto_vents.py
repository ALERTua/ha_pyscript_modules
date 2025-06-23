from imports import *
from pyscript_mock import *
from entities.entity import Entity

# # EXAMPLE
# HUMIDITY_VERYHIGH = 75.0
# HUMIDITY_HIGH = 65.0
# HUMIDITY_MID = 55.0
# HUMIDITY_LOW = 45.0
# IB_SHOWER_HUMIDITY_AUTO_FAN_ON = 'input_boolean.shower_humidity_auto_fan_on'
# IB_SHOWER_HUMIDITY_AUTO_FAN_OFF = 'input_boolean.shower_humidity_auto_fan_off'
#
#
# # SHOWER FAN AUTO ON
# @task_unique('func_shower_humidity_auto_fan_on', kill_me=True)
# @state_trigger(
#     f"{entity_exists(SHOWER_HUMIDITY, BEDROOM_HUMIDITY)} "
#     f" and float_({SHOWER_HUMIDITY}) >= {HUMIDITY_MID} "
#     f" and float_({SHOWER_HUMIDITY}) >= float_({BEDROOM_HUMIDITY}) + 10 ",
#     f"{entity_exists(BEDROOM_HUMIDITY)} and float_({BEDROOM_HUMIDITY}) >= {HUMIDITY_MID}",
#     f"{entity_exists(SHOWER_HUMIDITY)} and float_({SHOWER_HUMIDITY}) >= {HUMIDITY_VERYHIGH}",
#     watch=[
#         SHOWER_HUMIDITY,
#         BEDROOM_HUMIDITY,
#         IB_SHOWER_HUMIDITY_AUTO_FAN_ON,
#     ],
#     kwargs={
#         'actions': [
#             {
#                 'callable': f'homeassistant.turn_on, entity_id="{SHOWER_FAN}"',
#                 'wanted_entity_id': SHOWER_FAN,
#                 'wanted_state': 'on',
#                 'disable_notification': True,
#             },
#         ],
#     },
#     state_hold=30,
# )
# @conditional(
#     entity_on(IB_SHOWER_HUMIDITY_AUTO_FAN_ON),
#     entity_off(SHOWER_FAN),
#     entity_exists(SHOWER_HUMIDITY),
#     entity_exists(BEDROOM_HUMIDITY),
# )
# @time_active("range(8:00, 23:30)")
# def func_shower_humidity_auto_fan_on_day(trigger_type=None, var_name=None, value=None, old_value=None, context=None,
#                                          **kwargs):
#     return auto_vents(trigger_type=trigger_type, var_name=var_name, value=value, old_value=old_value, context=context,
#                       **kwargs)


def auto_vents(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    # log.debug(f"""{__name__}
    # trigger_type: {trigger_type}
    # var_name: {var_name}
    # value: {value}
    # """)
    # log.debug(f"{__name__}")
    actions = kwargs.get('actions', [])
    # if not all((trigger_type, var_name, value, actions)):
    #     log.debug(f"cannot condition monitor: args invalid: {trigger_type}, {var_name}, {value}, {actions}")
    #     return

    if not trigger_type == 'state':
        log.debug(f"cannot condition monitor: invalid trigger_type: {trigger_type}")
        return

    if isinstance(value, float):
        value = round(value, 2)

    for action in actions:
        wanted_entity_id = action.get('wanted_entity_id')
        trigger_name = kwargs.get('trigger', '')
        wanted_state = action.get('wanted_state')
        if not isinstance(wanted_entity_id, list):
            wanted_entity_id = [wanted_entity_id]

        for wanted_e_id in wanted_entity_id:
            wanted_entity = Entity(wanted_e_id)
            wanted_entity_friendly_name = wanted_entity.friendly_name()
            if trigger_name:
                trigger_name = f" {trigger_name}"
            if wanted_entity_id and wanted_state:
                current_state = wanted_entity.state()
                # log.debug(f"Current {wanted_entity_id} state: {current_state}")
                if wanted_state == current_state:
                    # log.debug(f"Nothing to do for {wanted_entity_friendly_name}")
                    continue

        tg_kwargs = {}
        chat_id = action.get('telegram_chat_id')
        if chat_id:
            tg_kwargs['target'] = chat_id

        disable_notification = action.get('disable_notification')
        if disable_notification is not None:
            tg_kwargs['disable_notification'] = disable_notification

        friendly_name = tools.friendly_name(var_name)
        func = action.get('func')
        func_kwargs = action.get('kwargs')
        callable_ = action.get('callable')
        if callable_:
            func_str = f"partial({callable_})"
            # log.debug(f"callable: {func_str}")
            func = eval(func_str)
            func.__name__ = callable_
            func_kwargs = {}

        if old_value is not None:
            lc_dt = old_value.last_changed
            lc = tools.dt_from_timestamp(lc_dt)
        else:
            lc = wanted_entity.last_changed()

        lc_str = tools.dt_to_datetime_string(lc)
        lc_now = tools.dt_diff(lc)

        wanted_entity_cur_state = wanted_entity.state()

        if func:
            funcname = func.__name__.replace('homeassistant.', '')
            func_kwargs_str = f" with {func_kwargs}" if func_kwargs else ''
            log.info(f"condition monitor for {wanted_entity_friendly_name} {var_name}"
                     f" @ {wanted_entity_cur_state}: executing {func.__name__}{func_kwargs_str}")
            msg = f"🪶{__name__}:\n" \
                  f"{friendly_name}> {trigger_type}{trigger_name} triggered on {var_name} value {value}. \n" \
                  f"{wanted_entity_friendly_name} was {wanted_entity_cur_state} " \
                  f"from {lc_str} \n" \
                  f"{lc_now} \n" \
                  f"Executing {funcname}{func_kwargs_str}"  # . \nWanted state: {wanted_state}
            if func_kwargs:
                func(**func_kwargs)
            else:
                func()
        else:
            msg = f"{friendly_name} {trigger_type}{trigger_name} triggered notification on value {value} \n" \
                  f"{wanted_entity_friendly_name} has been {wanted_entity_cur_state} " \
                  f"from {lc_str} \n" \
                  f"for {lc_now}"

        # if tg_kwargs:
        #     tools.telegram_message_alert_ha_private(msg=msg, **tg_kwargs)
        # else:
        #     tools.telegram_message_alert_ha_private(msg=msg)
        tools.discord_message(msg, target='1143090606835515432')
