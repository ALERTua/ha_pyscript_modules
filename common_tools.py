# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *

import traceback
import unicodedata as ud
from pendulum import DateTime
from pendulum.tz import Timezone

from mutagen.mp3 import MP3

latin_letters = {}


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


def telegram_message_alert_ha_public(msg=None, disable_notification=False, **kwargs):
    return telegram_message(
        msg=msg,
        disable_notification=disable_notification,
        target=TELEGRAM_CHAT_ALERT_HA,
        **kwargs
    )


def telegram_message_alert_ha_private(msg=None, disable_notification=False, **kwargs):
    return telegram_message(
        msg=msg,
        disable_notification=disable_notification,
        target=TELEGRAM_CHAT_ALERT_HA_PRIVATE,
        reply_to_message_id=7024,
        **kwargs
    )


def telegram_message(msg=None, disable_notification=True, **kwargs):
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

    msg_limit = 4096
    msgs = [msg[i:i + msg_limit] for i in range(0, len(msg), msg_limit)]
    for msg in msgs:
        telegram_bot.send_message(message=msg, disable_notification=disable_notification, **kwargs)


def telegram_video_url(url, caption=None, disable_notification=True, target=None, **kwargs):
    if not url:
        log.error("Couldn't send telegram video url: url is None or empty")
        return

    caption = caption or ''
    target = target or TELEGRAM_CHAT_ALERT_VIDEO
    return telegram_bot.send_video(url=url, caption=caption, supports_streaming=True,
                                   disable_notification=disable_notification, target=target, verify_ssl=False, **kwargs)


def telegram_photo(url, caption=None, disable_notification=True, **kwargs):
    if not url:
        log.error("Couldn't send telegram video url: url is None or empty")
        return

    caption = caption or ''
    return telegram_bot.send_photo(url=url, caption=caption, disable_notification=disable_notification, **kwargs)


def discord_message(msg, target=None, **kwargs):
    if not msg:
        log.error("Couldn't send discord message: msg is None or empty")
        return

    target = target or ["1093812584324530287"]
    if not isinstance(target, list):
        target = [target]

    target = [int(_) for _ in target]
    split = int(2000 * 0.9)
    messages = [msg[i: i + split] for i in range(0, len(msg), split)]
    for message in messages:
        # log.debug(f"Sending discord message len {len(message)}")
        notify.alert_iot(message=message, target=target, **kwargs)


def expand_sound_data(sound_name):
    sound_fullpath = MEDIA_PATH_BASE / sound_name
    sound_length = MP3(sound_fullpath).info.length
    sound_external_path = f"{SERVER_URL_EXTERNAL}{EXTERNAL_MEDIA_BASE}{sound_name}"
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
    func_name = getattr(func, '__name__', func)
    log.info(f"task_wait {func_name} {args}, {kwargs}")
    task_id = task.create(func, *args, **kwargs)
    done, pending = task.wait({task_id})
    # log.info(f"done {done}, pending {pending}")
    while not done:
        # log.info(f"done {done}, pending {pending}")
        task.sleep(0.1)
    log.info(f"task_wait {func_name} finished")


def wait_speaker_idle(entity_ids, state_check_now=False, state_hold=1.0, timeout=30):
    """
    https://hacs-pyscript.readthedocs.io/en/stable/reference.html#task-waiting
    """
    # log.info(f"wait_speaker_idle for {entity_ids}")
    if not isinstance(entity_ids, List):
        entity_ids = [entity_ids]
    entity_ids = list(set(entity_ids))
    idle_states = ('idle', 'on',)
    off_states = ('off', )
    statement = 'True'
    waiting = False
    output = []
    for entity_id in entity_ids:
        if (current_state := state.get(entity_id)) in off_states:
            # task_wait(media_player.turn_on, entity_id=entity_id)
            media_player.turn_on(entity_id=entity_id)
        elif current_state in UNK_O:
            continue
        elif current_state in idle_states:
            # task_wait(media_player.turn_on, entity_id=entity_id)
            media_player.turn_on(entity_id=entity_id)
            output.append(entity_id)
            continue
        # elif current_state == 'playing':
        #     continue

        output.append(entity_id)
        waiting = True
        # log.info(f"{entity_id} state: {state.get(entity_id)}")
        statement += f" and {entity_id} in {idle_states}"

    if not output:
        return output

    if waiting:
        log.debug(f"Waiting for {entity_ids} idle state with: {statement}")
    else:
        state_hold = None
        state_check_now = True
    # log.info(f"wait started {state_hold}")
    task.wait_until(statement, timeout=timeout, state_hold=state_hold, state_check_now=state_check_now)
    # log.info(f"wait finished")
    return output

    # log.debug(f"Entering {entity_id} idle state waiting. current state: {current_state}")
    # task.sleep(0.5)


def quiet_hours():
    return state.get('binary_sensor.quiet_hours') == 'on'
    # now = pendulum.now()
    # hours = now.hour
    # output = hours > QUIET_HOURS_START or hours < QUIET_HOURS_END
    # return output


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


def dt_to_pd(dt, timezone="local") -> DateTime:
    if isinstance(dt, float):
        timestamp = dt
    else:
        timestamp = dt.timestamp()
    return pendulum.from_timestamp(timestamp, tz=timezone)


def pd_diff(pd, timezone="local"):
    now = pendulum.now(tz=timezone)
    if now > pd:
        return now - pd

    return pd - now


def pd_words(pd, locale='ua'):
    try:
        return pd.in_words(locale=locale)
    except Exception as e:
        log.warning(f"Exception converting pd_words to {locale}: {type(e)} {e}")
        return pd.in_words()


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


def speak_language_from_code(lang_code):
    if lang_code in ('ua', ):
        voice = choice(
            (
                'uk-UA-PolinaNeural', 
                'uk-UA-OstapNeural'
            )
        )
    else:
        voice = choice(
            (
                'en-AU-NatashaNeural',
                'en-AU-WilliamNeural',
                'en-CA-ClaraNeural',
                'en-CA-LiamNeural',
                'en-GB-LibbyNeural',
                'en-GB-MaisieNeural',
                'en-GB-RyanNeural',
                'en-GB-SoniaNeural',
                'en-GB-ThomasNeural',
                'en-US-AnaNeural',
                'en-US-AriaNeural',
                'en-US-ChristopherNeural',
                'en-US-EricNeural',
                'en-US-GuyNeural',
                'en-US-JennyNeural',
                'en-US-MichelleNeural',
            )
        )
    return voice


def fstr(template_):
    output = eval(f"f'''{template_}'''")
    return output


def is_latin(uchr):
    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))


def only_roman_chars(unistr):
    for uchr in unistr:
        if uchr.isalpha() and not is_latin(uchr):
            return False

    return True
    # return all(is_latin(uchr) for uchr in unistr if uchr.isalpha())


def round_temp_float(temp_float, precision=0.5, round_result=1):
    temp_float = float(temp_float)
    return round(round(temp_float / precision, 0) * precision, round_result)


def notify_alert_mob(message, *args, **kwargs):
    notify.mobile_app_alert_s_s24(message=message, *args, **kwargs)
