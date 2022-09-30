# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *  # cyclic
import common_tools as tools

registered_telegram_callbacks = []


def register_telegram_callback(action, remove_markup=False, add_text=None):
    log.debug(f"{__name__}: {tools.func_name()}: {action}")
    timestamp = str(pendulum.now('local').timestamp).replace('.', '')
    task_name = f"tg_cb_{timestamp}_{randint(0, 99999)}"

    @event_trigger('telegram_callback')
    def fnc(**kwargs):
        task.unique(task_name, kill_me=True)
        button_action = kwargs.get('data')
        if button_action != task_name:
            # log.debug(f"cannot process {task_name}. no button_action")
            return

        tools.try_execute(action)
        id_ = kwargs.get('id')
        if id_:
            telegram_bot.answer_callback_query(callback_query_id=id_, message="Done", show_alert=False)

        if fnc in registered_telegram_callbacks:
            registered_telegram_callbacks.remove(fnc)
            log.debug(f"{fnc} kwargs: {tools.pformat(kwargs)}")
            message = kwargs.get('message', dict())
            message_id = message.get('message_id')
            chat_id = message.get('chat', {}).get('id')
            if remove_markup and message:
                telegram_bot.edit_replymarkup(message_id=message_id, chat_id=chat_id, inline_keyboard=[])
            if add_text and message:
                text = message.get('text', '')
                result_text = text + add_text
                telegram_bot.edit_message(message_id=message_id, chat_id=chat_id, message=result_text)
        # log.debug(f"registered_telegram_callbacks left: {registered_telegram_callbacks}")

    # log.debug(f"Registering {task_name}")
    registered_telegram_callbacks.append(fnc)
    return task_name
