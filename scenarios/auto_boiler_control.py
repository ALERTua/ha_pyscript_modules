from imports import *
from pyscript_mock import *
from entities.water_heater import WaterHeater

DISCORD_CHATS = ['1262407979920261161']


def auto_boiler_control(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    dbg = True
    ib_eid = kwargs.get('IB_EID', None)
    discount_period_eid = kwargs.get('DISCOUNT_PERIOD_EID', None)
    boiler_eid = kwargs.get('BOILER_EID', None)
    ignore_boiler_off = kwargs.get('IGNORE_BOILER_OFF', False)
    discount_on_mode = kwargs.get('DISCOUNT_ON_MODE', 'eco')
    discount_off_mode = kwargs.get('DISCOUNT_OFF_MODE', 'eco')

    if any([_ for _ in (ib_eid, discount_period_eid, boiler_eid) if _ is None]):
        log.error(f"{__name__} not all args are set:\n{pformat(locals())}")
        return

    ib_e = entity(ib_eid)
    discount_period_e = entity(discount_period_eid)
    boiler_e = WaterHeater(boiler_eid)
    boiler_mode_current = boiler_e.state()
    boiler_is_off = boiler_e.is_off()
    boiler_away_mode_on = boiler_e.away_mode_on()
    if not ignore_boiler_off and (boiler_is_off or boiler_away_mode_on):
        if dbg:
            log.debug(f"{__name__}: boiler is off and ignore_boiler_off is not set. Not doing anything.")
        return

    e_checks = (
        (ib_eid, ib_e),
        (discount_period_eid, discount_period_e),
        (boiler_eid, boiler_e),
    )
    for eid, e in e_checks:
        if e is None:
            log.error(f"{__name__}: entity not found: {eid}")
            return

    discount_period_on = discount_period_e.is_on()
    boiler_mode_needed = discount_on_mode if discount_period_on else discount_off_mode
    if boiler_mode_current == boiler_mode_needed:
        msg = f"{__name__}: discount_period: {discount_period_on}. boiler_mode_needed: {boiler_mode_needed} == {boiler_mode_current}. Nothing to do."
    else:
        msg = f"{__name__}: discount_period: {discount_period_on}. boiler_mode_needed: {boiler_mode_needed} vs {boiler_mode_current}. Setting mode to {boiler_mode_needed}."
        boiler_e.set_operation_mode(boiler_mode_needed)

    log.debug(msg)
    tools.discord_message(msg, target=DISCORD_CHATS)
