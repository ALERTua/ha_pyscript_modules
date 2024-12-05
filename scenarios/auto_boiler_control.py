from imports import *
from pyscript_mock import *
from entities.water_heater import WaterHeater

DISCORD_CHATS = ['1262407979920261161']


def auto_boiler_control(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    dbg = False
    discount_period_eid = kwargs.get('DISCOUNT_PERIOD_EID', None)
    boiler_eid = kwargs.get('BOILER_EID', None)
    ignore_boiler_off = kwargs.get('IGNORE_BOILER_OFF', False)
    discount_on_mode = kwargs.get('MODE_DISCOUNT', 'performance')
    discount_off_mode = kwargs.get('MODE', 'eco')
    target_temperature_eid = kwargs.get('TARGET_TEMPERATURE_EID', 'number.boiler_target_temperature')
    target_temperature_discount = kwargs.get('TARGET_TEMPERATURE_DISCOUNT', 65)
    target_temperature = kwargs.get('TARGET_TEMPERATURE', 55)
    showers_eid = kwargs.get('SHOWERS_EID', 'number.boiler_expected_number_of_shower')
    showers_discount = kwargs.get('SHOWERS_DISCOUNT', 5)
    showers = kwargs.get('SHOWERS', 4)
    force_on = kwargs.get('FORCE_ON', False)
    trigger_name = kwargs.get('TRIGGER')

    if any([_ for _ in (discount_period_eid, boiler_eid) if _ is None]):
        log.error(f"{__name__} not all args are set:\n{pformat(locals())}")
        return

    discount_period_e = entity(discount_period_eid)
    boiler_e = WaterHeater(boiler_eid)
    boiler_mode_current = boiler_e.state()
    boiler_is_off = boiler_e.is_off()
    boiler_away_mode_on = boiler_e.away_mode_on()
    if not ignore_boiler_off and (boiler_is_off or boiler_away_mode_on):
        if dbg:
            log.debug(f"{__name__}: boiler is off and ignore_boiler_off is not set. Not doing anything.")
        return

    target_temperature_e = entity(target_temperature_eid)
    target_temperature_current = float_(target_temperature_e.state())
    showers_e = entity(showers_eid)
    showers_current = int_(showers_e.state())

    e_checks = (
        (discount_period_eid, discount_period_e),
        (boiler_eid, boiler_e),
        (target_temperature_eid, target_temperature_e),
        (showers_eid, showers_e),
    )
    for eid, e in e_checks:
        if e is None:
            msg = f"{__name__}: entity not found: {eid}"
            log.error(msg)
            tools.telegram_message_alert_ha_private(msg)
            return

    discount_period_on = discount_period_e.is_on()
    boiler_mode_needed = discount_on_mode if discount_period_on else discount_off_mode
    boiler_mode_needed = discount_on_mode if force_on else boiler_mode_needed
    showers_needed = showers_discount if discount_period_on else showers
    temperature_needed = target_temperature_discount if discount_period_on else target_temperature

    msg = f'💧🔥{__name__}:\nforce_on: {force_on}'
    if trigger_name:
        msg += f'\ntrigger_name: {trigger_name}'

    msg += f'\ndiscount_period: {discount_period_on}'
    action_taken = False
    if boiler_mode_current != boiler_mode_needed:
        msg += f"\nboiler_mode_needed: {boiler_mode_needed} vs {boiler_mode_current}.\nSetting mode to {boiler_mode_needed}."
        boiler_e.set_operation_mode(boiler_mode_needed)
        action_taken = True

    if showers_current != showers_needed:
        msg += f"\nshowers_needed: {showers_needed} vs {showers_current}.\nSetting showers to {showers_needed}."
        showers_e.set_value(showers_needed)
        action_taken = True

    if target_temperature_current != temperature_needed:
        msg += f"\ntemperature_needed: {temperature_needed} vs {target_temperature_current}.\nSetting temperature to {temperature_needed}."
        target_temperature_e.set_value(temperature_needed)
        action_taken = True

    if action_taken:
        log.debug(msg)
        tools.discord_message(msg, target=DISCORD_CHATS)
