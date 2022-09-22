# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *
import constants
import traceback
from mutagen.mp3 import MP3


def state_bool(state_):
    on_states = ['on', ]
    off_states = ['off', ]
    state_ = state_.lower()
    if state_ in on_states:
        return True
    elif state_ in off_states:
        return False
    else:
        return None


def telegram_message_alert_ha(msg=None, disable_notification=False, **kwargs):
    return telegram_message(msg=msg, disable_notification=disable_notification, target=constants.TELEGRAM_CHAT_ALERT_HA,
                            **kwargs)


def telegram_message(msg=None, disable_notification=False, **kwargs):
    # inline = [
    #     [
    #         ["Text btn1", "/button1"], 
    #         ["Text btn2", "/button2"]
    #     ], 
    #     [
    #         ["Text btn3", "/button3"]
    #     ]
    # ]
    # tools.telegram_message('test', inline_keyboard=inline)
    if not msg:
        log.error("Couldn't send telegram message: msg is None or empty")
        return

    try:
        return service.call('telegram_bot', 'send_message', message=msg, disable_notification=disable_notification,
                            **kwargs)
    except Exception as e:
        log.exception("Error sending telegram message", exc_info=e)


def telegram_video_url(url=None, caption=None, disable_notification=False, **kwargs):
    if not url:
        log.error("Couldn't send telegram video url: url is None or empty")
        return

    return service.call('telegram_bot', 'send_video', url=url, caption=caption,
                        disable_notification=disable_notification, **kwargs)


def telegram_photo(url=None, caption=None, disable_notification=False, **kwargs):
    if not url:
        log.error("Couldn't send telegram video url: url is None or empty")
        return

    return service.call('telegram_bot', 'send_photo', url=url, caption=caption,
                        disable_notification=disable_notification, **kwargs)


def discord_message(msg=None):
    if not msg:
        log.error("Couldn't send discord message: msg is None or empty")
        return

    split = 1500
    messages = [msg[i: i + split] for i in range(0, len(msg), split)]
    for message in messages:
        log.debug(f"Sending discord message len {len(message)}")
        service.call('script', 'discord_say', message=message)


def expand_sound_data(sound_name):
    sound_fullpath = constants.MEDIA_PATH_BASE / sound_name
    sound_length = MP3(sound_fullpath).info.length
    sound_external_path = f"{constants.SERVER_URL_EXTERNAL}{constants.EXTERNAL_MEDIA_BASE}{sound_name}"
    # log.debug(f"expand sound data for {sound_name}: {sound_external_path}")
    return sound_fullpath, sound_length, sound_external_path


def speaker_toggle(entity_id, on=True):
    output = None
    if on and state.get(entity_id) in ('off',):
        output = media_player.turn_on(entity_id=entity_id)
    elif not on and state.get(entity_id) not in ('off',):
        output = media_player.turn_off(entity_id=entity_id)
    return output


def task_wait(func, *args, **kwargs):
    task_id = task.create(func, *args, **kwargs)
    task.wait([task_id])


def wait_speaker_idle(entity_id, state_check_now=True, state_hold=0.5, timeout=None):
    """
    https://hacs-pyscript.readthedocs.io/en/stable/reference.html#task-waiting
    """

    if (current_state := state.get(entity_id)) in ('off', ):
        media_player.turn_on(entity_id=entity_id)

    # log.debug(f"Entering {entity_id} idle state waiting. current state: {current_state}")
    # task.sleep(0.5)
    return task.wait_until(f"{entity_id} == 'idle'", timeout=timeout, state_hold=state_hold,
                           state_check_now=state_check_now)


def quiet_hours():
    now = pendulum.now()
    hours = now.hour
    output = hours > constants.QUIET_HOURS_START or hours < constants.QUIET_HOURS_END
    return output


def friendly_name(entity_id):
    if entity_id:
        attrs = state.getattr(entity_id)
        if attrs:
            return attrs.get('friendly_name') or entity_id
        else:
            return entity_id
    
    return ''


def debug(ip='192.168.1.2', port=12345):
    try:
        # pylint: disable=import-error
        import pydevd_pycharm  # noqa: E402
    except:
        import os
        os.system('pip install -U pydevd-pycharm')
        return debug(ip=ip, port=port)

    log.debug(f"Connecting to PyCharm Debugger @ {ip}:{port}")
    try:
        pydevd_pycharm.settrace(ip, port=port, stdoutToServer=True, stderrToServer=True, suspend=False)
    except Exception as e:
        log.debug(f"Error connecting to PyCharm Debugger @ {ip}:{port} : {type(e)} {e}")
        return

    log.debug(f"Connected to PyCharm Debugger @ {ip}:{port}")


def filename_timestamp():
    return "%s" % timestamp_to_date()


def timestamp_to_date(timestamp=None, _format='%Y-%m-%d_%H-%M-%S', timezone="local"):
    """

    :param _format: date format
    :param timezone: date timezone
    :type timestamp: int or float
    :rtype: str
    """
    if isinstance(timestamp, (str, int, float)):
        # noinspection PyTypeChecker
        timestamp = pendulum.from_timestamp(timestamp, tz=timezone)
    elif isinstance(timestamp, type(None)):
        # noinspection PyTypeChecker
        timestamp = pendulum.now(tz=timezone)
    output = timestamp.strftime(_format)
    return output


def func_name():
    return traceback.extract_stack(None, 2)[0][2]


def print_var(var):
    log.debug(f"print_var type: {type(var)}")
    try:
        log.debug(f"print_var: {pformat(var)}")
    except:
        log.debug(f"print_var: {var}")
    log.debug(f"print_var dir : {pformat(dir(var))}")


def try_execute(action):
    log.debug(f"{__name__}: try_execute: {action}")
    try:
        exec(action)
    except Exception as e:
        log.warning(f"""Error executing action
action: {action}
exception: {type(e)} {e}""")

