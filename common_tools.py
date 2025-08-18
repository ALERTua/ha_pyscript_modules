# https://hacs-pyscript.readthedocs.io/en/stable/reference.html
from imports_base import *
import math
import requests
import unicodedata as ud
from datetime import datetime
import humanize
from entities.ha import HA
from mutagen.mp3 import MP3

latin_letters = {}

ha = HA()


def state_bool(state_):
    if state_ is None:
        return None

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


def telegram_message_alert_ha_private(msg=None, disable_notification=True, **kwargs):
    return telegram_message(
        msg=msg,
        disable_notification=disable_notification,
        target=TELEGRAM_CHAT_ALERT_HA_PRIVATE,
        reply_to_message_id=7024,
        **kwargs
    )


def telegram_message(msg=None, disable_notification=True, **kwargs):  # message_thread_id
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

    kwargs.setdefault('parse_mode', 'markdown')
    kwargs.setdefault('disable_web_page_preview', False)

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
    return telegram_bot.send_video(url=url, caption=caption, disable_notification=disable_notification, target=target,
                                   verify_ssl=False, **kwargs)


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

    target = target or [DISCORD_CHANNEL_HA]
    if not isinstance(target, list):
        target = [target]

    target = [int(_) for _ in target]
    split = int(2000 * 0.9)
    messages = [msg[i: i + split] for i in range(0, len(msg), split)]
    for message in messages:
        # log.debug(f"Sending discord message len {len(message)}")
        try:  # errors during ha relaunch
            notify.alert_iot(message=message, target=target, **kwargs)
        except:
            pass


def expand_sound_data(sound_name):
    sound_fullpath = MEDIA_PATH_BASE / sound_name
    mp3 = MP3(sound_fullpath)
    mp3_info = mp3.info
    sound_length = mp3_info.length
    sound_external_path = sound_ext_path(sound_name)
    # log.debug(f"expand sound data for {sound_name}: {sound_external_path}")
    return sound_fullpath, sound_length, sound_external_path


def sound_ext_path(sound_name):
    output = f"{SERVER_URL_EXTERNAL}{EXTERNAL_MEDIA_BASE}{sound_name}"
    return output


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
    log.info(f"done {done}, pending {pending}")
    while pending or not done:
        log.info(f"done {done}, pending {pending}")
        task.sleep(0.1)
    log.info(f"task_wait {func_name} finished")


def wait_speaker_idle(entity_ids, state_check_now=True, state_hold=0.5, timeout=30):
    """
    https://hacs-pyscript.readthedocs.io/en/stable/reference.html#task-waiting
    """
    # log.info(f"wait_speaker_idle for {entity_ids}")
    if not isinstance(entity_ids, List):
        entity_ids = [entity_ids]
    entity_ids = list(set(entity_ids))
    idle_states = ('idle', 'on',)
    off_states = ('off',)
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


def speaker_play_file(speaker_entity_ids, filename, media_content_type='audio/mp3', **kwargs):
    pre_snd_ext_path = sound_ext_path(filename)
    return media_player.play_media(entity_id=speaker_entity_ids, media_content_type=media_content_type,
                                   media_content_id=pre_snd_ext_path, **kwargs)

def mass_play_file(speaker_entity_ids, filename, use_pre_announce=False):
    pre_snd_ext_path = sound_ext_path(filename)
    # noinspection PyTypeChecker
    return music_assistant.play_announcement(
        entity_id=speaker_entity_ids,
        url=pre_snd_ext_path,
        use_pre_announce=use_pre_announce,
    )
    # return media_player.play_media(entity_id=speaker_entity_ids, media_content_type=media_content_type,
    #                                media_content_id=pre_snd_ext_path, **kwargs)

def quiet_hours():
    return state.get('binary_sensor.quiet_hours') == 'on'
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


# def debug(ip='192.168.1.2', port=12345):
#     try:
#         # pylint: disable=import-error
#         import pydevd_pycharm  # noqa: E402
#     except:
#         import os
#         os.system('pip install -U pydevd-pycharm')
#         return debug(ip=ip, port=port)
#
#     log.debug(f"Connecting to PyCharm Debugger @ {ip}:{port}")
#     try:
#         pydevd_pycharm.settrace(ip, port=port, stdoutToServer=True, stderrToServer=True, suspend=False)
#     except Exception as e:
#         log.debug(f"Error connecting to PyCharm Debugger @ {ip}:{port} : {type(e)} {e}")
#         return
#
#     log.debug(f"Connected to PyCharm Debugger @ {ip}:{port}")


def timedelta_words(value: timedelta | float, months: bool = True, minimum_unit: str = "seconds", locale: str = 'uk_UA') -> str:
    if locale == 'en':
        task.executor(humanize.i18n.deactivate)
    else:
        task.executor(humanize.i18n.activate, locale)
    return humanize.naturaldelta(value, months=months, minimum_unit=minimum_unit)


def dt_words(value: datetime | timedelta | float,
             future: bool = False,
             months: bool = True,
             minimum_unit: str = "seconds",
             when: datetime | None = None,
             locale: str = 'uk_UA') -> str:
    if locale == 'en':
        task.executor(humanize.i18n.deactivate)
    else:
        task.executor(humanize.i18n.activate, locale)
    return humanize.naturaltime(value, future=future, months=months, minimum_unit=minimum_unit, when=when)


def filename_timestamp():
    return "%s" % timestamp_to_date()


def timestamp_to_date(timestamp: datetime | int | float | None = None, _format: str = '%Y-%m-%d_%H-%M-%S') -> str:
    """
    Convert a timestamp (datetime, int, or float) to a formatted date string.

    :param timestamp: The timestamp to convert (defaults to the current time if None).
    :param _format: The format string for the output date (default: '%Y-%m-%d_%H-%M-%S').
    :return: Formatted date string.
    """
    if timestamp is None:
        timestamp = datetime.now()
    elif isinstance(timestamp, (int, float)):
        timestamp = datetime.fromtimestamp(timestamp)
    elif isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)

    return timestamp.strftime(_format)


def dt_from_timestamp(timestamp):
    if isinstance(timestamp, str):
        timestamp = float(timestamp)
    if isinstance(timestamp, float):
        timestamp = timestamp
    else:
        timestamp = timestamp.timestamp()
    return datetime.fromtimestamp(timestamp, tz=ha.time_zone())


def dt_diff(dt: datetime) -> timedelta:
    now = datetime.now(tz=ha.time_zone())
    if now > dt:
        return now - dt

    return dt - now


def dt_to_datetime_string(dt: datetime = None) -> str:
    if dt is None:
        dt = datetime.now(tz=ha.time_zone())

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def timedelta_hours(td: timedelta) -> float:
    return td.total_seconds() / 3600.0


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


def tts_edge_voice_from_language_code(lang_code):
    if lang_code in ('ua',):
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


def fstr(template_: str, locals_dict: dict):
    # output = eval(f"f'''%s'''" % template_, __locals=locals_dict or dict())
    dct = copy(locals())
    dct.update(locals_dict)
    output = '%s' % template_
    output = output.format(**dct)
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


# round to closest precision, then round to round_result
def round_temp_float(temp_float, precision=0.5, round_result=1):
    temp_float = float(temp_float)
    return round(round(temp_float / precision, 0) * precision, round_result)


# round down to closest precision, then round to round_result
def round_down(value, precision=1.0, round_result=None):
    result = math.floor(float(value) / precision) * precision
    return round(result, round_result) if round_result is not None else result


# round up to closest precision, then round to round_result
def round_up(value, precision=1.0, round_result=None):
    result = math.ceil(float(value) / precision) * precision
    return round(result, round_result) if round_result is not None else result


def converse_stringify_numbers(txt, agent_id=LLM_STANDARD, language='UA', conversation_id=''):
    prompt = f"""
    тобі буде надано фразу, що містить цифри 
    перепиши цю фразу прописом, замінюючи цифри на їх прописну версію написання.
    наприклад "сьогодні 1001 день війни" треба переписати так: "Сьогодні тисяча перший день війни"
    наприклад "я не бачу 3 помідорів" треба переписати так: "я не бачу трьох помідорів"
    наприклад "це сталося у 1220 році" треба переписати так: "це сталося у тисяча двісті двадцятому році"
    Ось сама фраза:
    {txt}"""
    return converse(prompt, agent_id=agent_id, language=language, conversation_id=conversation_id)

def converse(txt, agent_id=LLM_STANDARD, language='UA', conversation_id=''):
    log.debug(f"Conversing {language} {agent_id}\n{txt}\n___")
    # noinspection PyArgumentList
    response = conversation.process(agent_id=agent_id, language=language, text=txt,
                                    conversation_id=conversation_id, return_response=True) or {}
    """
    {
        'conversation_id': '01J4PM01TN6X0JKXKY4VS2Q792', 
        'response': {
            'card': {},
            'data': {
                'failed': [], 
                'success': [], 
                'targets': []
            }, 
            'language': 'UA',
            'response_type': 'action_done', 
            'speech': {
                'plain': {
                    'extra_data': None,
                    'speech': 'Південно-східне напрямку України. Загроза авіаційного удару.'
                }
            }
        }
    }
    """
    answer = response.get('response', {}).get('speech', {}).get('plain', {}).get('speech', '')
    log.debug(f"Conversation answer for {language} {agent_id}\n{answer}")
    return answer, response


PROVIDER = "01JDEV89KBVTW1F5V2X70GTD51"
MODEL = "llama3.2-vision:11b-instruct-q4_K_M"

PROMPT = """
Ти — спеціаліст із моніторингу камер спостереження.
Твоє завдання — створювати короткий підсумок активності, що відбувається на серії послідовних кадрів із відеозапису.

Ти повинен:
1. Ігнорувати будь-які деталі, пов'язані з інтер'єром, будівлею, підлогою, стінами, дверима, вікнами та іншими статичними об'єктами.
2. Якщо на кадрах немає активності (руху, подій), ти маєш відповісти: "На кадрах активність відсутня."  
3. Якщо активність є, об'єднай усю інформацію в **одне речення**, описуючи події стисло, без покадрового аналізу.  

Головні принципи:  
- Чіткість і лаконічність.
- Без пояснень, деталей інтер'єру чи покадрових перерахувань.
- Відповіді мають бути українською мовою.

Приклад:  
Кадри не містять активності. Відповідь: "На кадрах активність відсутня."  
"""

async def converse_frigate_event(
        event_id: str,
        provider: str = PROVIDER,
        message: str = PROMPT,
        include_filename: bool = True,
        max_tokens: int = 250,
        temperature: float = 0.3,
        model: str = MODEL,
        remember: bool = True,
        video_file: str = "",
        max_frames: int = 10,
        target_width: int = 3840,
        detail: Literal['', 'high', 'low'] = '',
        expose_images: bool = False,
):
    output = llmvision.video_analyzer(
        event_id=event_id,
        provider=provider,
        message=message,
        include_filename=include_filename,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model,
        remember=remember,
        # video_file=video_file,
        max_frames=max_frames,
        # target_width=target_width,
        # detail=detail,
        expose_images=expose_images,
    ) or {}
    response_text = output.get('response_text', '')
    log.debug(f"{model} response for {event_id}:\n{response_text}")
    return response_text


def got_power():
    pwr = state.get(POWER)
    return pwr != 'off'


def got_internet():
    inet = state.get(INTERNET)
    return inet != 'off'


# create a decorator that try-excepts the function and if it fails, it will call the function again
def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.warning(f"{func.__name__} failed: {type(e)} {e}")

    return wrapper


def check_mp4_file(url):
    try:
        # Send a GET request with streaming to avoid downloading the entire file
        response = task.executor(requests.get, url=url, verify=False, stream=True, timeout=10)

        # Check HTTP status code
        if response.status_code != 200:
            return False, f"Error: Received HTTP {response.status_code} for {url}"

        # Check Content-Type
        content_type = response.headers.get("Content-Type", "")
        if "video/mp4" not in content_type:
            return False, f"Error: Content-Type {content_type} is not video/mp4"

        # Check the content signature (first few bytes of the file)
        # Reading the first 8 bytes to verify MP4 signature
        file_signature = next(response.iter_content(8))
        if file_signature[:4] != b'\x00\x00\x00\x18' and file_signature[4:8] != b'ftyp':
            return False, "Error: File does not have a valid MP4 signature."

        return True, "Success: URL contains a valid MP4 file."
    except Exception as e:
        return False, f"Request failed: {type(e)} {e}"
