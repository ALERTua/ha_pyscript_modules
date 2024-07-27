# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *  # cyclic
from entities.entity import entity
from entities.ha import HA

state.persist(TELEGRAM_CALLBACKS)


def register_telegram_callback(actions, remove_markup=False, add_text=None):
    tstamp = pendulum.now('local').timestamp()
    timestamp = str(tstamp).replace('.', '')
    task_name = f"tg_cb_{timestamp}_{randint(0, 999)}"
    if not isinstance(actions, list):
        actions = [actions]

    telegram_callbacks = entity(TELEGRAM_CALLBACKS)
    telegram_callbacks.setattr(
        task_name,
        dict(
            timestamp=tstamp,
            actions=actions,
            remove_markup=remove_markup,
            add_text=None,
        )
    )

    telegram_callbacks = entity(TELEGRAM_CALLBACKS)
    return task_name


# @state_trigger(TEST_BOOLEAN)
@time_trigger(TIME_TRIGGER_HOURLY)
def remove_telegram_callbacks(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    ha = HA()
    ent = entity(TELEGRAM_CALLBACKS)
    attrs = ent.attrs()
    # log.info(f"remove_telegram_callbacks start")
    for cb_name, kb_dict in attrs.items():
        cb_timestamp = kb_dict.get('timestamp')
        cb_date = ha.datetime_p(cb_timestamp)
        date_diff = ha.datetime_p() - cb_date
        cb_delete =  date_diff.in_hours() > 24
        if cb_delete:
            log.info(f"{cb_name}: hours: {date_diff.in_hours()} delete: {cb_delete}")
            ent.delattr(cb_name)

    # log.info(f"remove_telegram_callbacks done")


@service
def wipe_telegram_callbacks(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    log.info(f"Wiping telegram callbacks")
    state.set(TELEGRAM_CALLBACKS, new_attributes=dict())
