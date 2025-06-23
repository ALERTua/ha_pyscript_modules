# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *  # cyclic
import common_tools as tools
from entities.entity import entity
from entities.ha import HA

state.persist(ACTION_CALLBACKS)


def register_telegram_callback(actions, remove_markup=False, add_text=None):
    tstamp = dt_util.now().timestamp()
    timestamp = str(tstamp).replace('.', '')
    task_name = f"tg_cb_{timestamp}_{randint(0, 999)}"
    if not isinstance(actions, list):
        actions = [actions]

    action_callbacks = entity(ACTION_CALLBACKS)
    action_callbacks.setattr(
        task_name,
        dict(
            timestamp=tstamp,
            actions=actions,
            remove_markup=remove_markup,
            add_text=None,
        )
    )

    action_callbacks = entity(ACTION_CALLBACKS)
    return task_name


# @state_trigger(TEST_BOOLEAN)
@time_trigger(TIME_TRIGGER_HOURLY)
def remove_callbacks(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    ha = HA()
    ent = entity(ACTION_CALLBACKS)
    attrs = ent.attrs()
    # log.info(f"remove_callbacks start")
    for cb_name, kb_dict in attrs.items():
        cb_timestamp = kb_dict.get('timestamp')
        cb_date = tools.dt_from_timestamp(cb_timestamp)
        date_diff = ha.datetime() - cb_date

        hours = tools.timedelta_hours(date_diff)
        cb_delete = hours > 24
        if cb_delete:
            log.info(f"{cb_name}: hours: {hours} delete: {cb_delete}")
            ent.delattr(cb_name)

    # log.info(f"remove_callbacks done")


@service
def wipe_callbacks(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    log.info(f"Wiping action callbacks")
    state.set(ACTION_CALLBACKS, new_attributes=dict())
