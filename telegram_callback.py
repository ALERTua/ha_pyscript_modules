# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *  # cyclic
from entities.entity import entity

state.persist(TELEGRAM_CALLBACKS)


def register_telegram_callback(actions, remove_markup=False, add_text=None):
    tstamp = pendulum.now('local').timestamp()
    timestamp = str(tstamp).replace('.', '')
    task_name = f"tg_cb_{timestamp}_{randint(0, 999)}"
    # log.debug(f'tg cb task_name: {task_name}')

    # @event_trigger('telegram_callback')  # f"data == '{task_name}'"
    # def fnc(trigger_type=None, event_type=None, context=None, id=None, chat_instance=None, data=None, message=None,
    #         chat_id=None, user_id=None, from_first=None, from_last=None):
    #
    #     # if data != task_name:
    #     #     return
    #
    #     task.unique(data)
    #     log.debug(f"{task_name} triggered with data: {data}")
    #     return
    #     log.debug(f"telegram callback triggered: {task_name}:\n{pformat(args)}\n{pformat(kwargs)}")
    #     return
    #     nonlocal actions
    #     nonlocal registered_telegram_callbacks
    #     log.debug(f"telegram_callback trigger: {task_name}: {kwargs}")
    #     button_action = kwargs.get('data')
    #     # if button_action != task_name:
    #     #     # log.debug(f"cannot process {task_name}. no button_action")
    #     #     return
    #
    #
    #     if not isinstance(actions, list):
    #         actions = [actions]
    #
    #     for action in actions:
    #         tools.try_execute(action)
    #
    #     id_ = kwargs.get('id')
    #     if id_:
    #         telegram_bot.answer_callback_query(callback_query_id=id_, message="Done", show_alert=False)
    #
    #     if fnc in registered_telegram_callbacks:
    #         registered_telegram_callbacks.remove(fnc)
    #         log.debug(f"{fnc} kwargs: {tools.pformat(kwargs)}")
    #         message = kwargs.get('message', dict())
    #         message_id = message.get('message_id')
    #         chat_id = message.get('chat', {}).get('id')
    #         if remove_markup and message:
    #             telegram_bot.edit_replymarkup(message_id=message_id, chat_id=chat_id, inline_keyboard=[])
    #         if add_text and message:
    #             text = message.get('text', '')
    #             result_text = text + add_text
    #             telegram_bot.edit_message(message_id=message_id, chat_id=chat_id, message=result_text)
    #     # log.debug(f"registered_telegram_callbacks left: {registered_telegram_callbacks}")

    if not isinstance(actions, list):
        actions = [actions]

    # log.debug(f"Registering Telegram Callback {task_name}")
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
