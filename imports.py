import common_tools as tools
from action_callback import register_telegram_callback
from imports_base import *

from entities.entity import entity
from entities.ha import HA
from entities.msg_bucket import MsgBucket, DiscordMsgBucket
from homeassistant.const import EVENT_CALL_SERVICE
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
import homeassistant.helpers.template as template
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/entity.py
import homeassistant.helpers.entity as entity_helper

ha = HA()


def entity_not_exists(entity_id):
    _ = entity(entity_id)
    # return f"hass.states.get(f'{entity_id}') in {UNK_S} "
    # return f"{entity_id} in {UNK_S} "
    return f"(hass.states.get('{entity_id}') in {UNK_S}) "


def entity_exists_1(entity_id, debug=False):
    _ = entity(entity_id)
    output = f"(hass.states.get('{entity_id}') not in {UNK_S} and {entity_id} not in {UNK_S}) "
    if debug:
        log.debug(f"entity_exists: {output} entity {entity_id} state: {hass.states.get(entity_id)}")

    return output
    # return f"{entity_id} not in {UNK_S} "
    # return f"hass.states.get('{entity_id}') is not None "


def entity_exists(*entity_ids, debug=False):
    if len(entity_ids) == 1:
        return entity_exists_1(entity_ids[0], debug=debug)

    output = ''
    for entity_id in entity_ids:
        _ = entity(entity_id)
        if output:
            output += " and "
        output += entity_exists_1(entity_id)

    if debug:
        log.debug(f"entity_exists: {output}")
        for entity_id in entity_ids:
            log.debug(f"entity {entity_id} state: {hass.states.get(entity_id)}")
    return output


def entity_on(entity_id, debug=False):
    e = entity(entity_id)
    if debug:
        estate = e.state()
        log.debug(f"entity_on for {entity_id}: {e}: {estate}")

    return f"(hass.states.get('{entity_id}') in ('on', 'home') or {entity_id} in ('on', 'home')) "
    # return f"{entity_id} in ('on', 'home') "


def entity_not_on(entity_id):
    _ = entity(entity_id)
    # return f"(hass.states.get('{entity_id}') not in ('on', 'home') or {entity_id} not in ('on', 'home')) "
    return f"{entity_id} not in ('on', 'home') "


def entity_off(entity_id):
    _ = entity(entity_id)
    return f"(hass.states.get('{entity_id}') in ('off', 'away') or {entity_id} in ('off', 'away')) "
    # return f"{entity_id} in ('off', 'away') "


def entity_not_off(entity_id):
    _ = entity(entity_id)
    # return f"(hass.states.get('{entity_id}') not in ('off', 'away') or {entity_id} not in ('off', 'away'))"
    return f"{entity_id} not in ('off', 'away') "


def speaker_idle(entity_id):
    _ = entity(entity_id)
    return f"(hass.states.get('{entity_id}') in ('off', 'on', 'idle') or {entity_id} in ('off', 'on', 'idle'))"
    # return f"{entity_id} in ('off', 'on', 'idle') "


def entity_last_seen_not_older_than(entity_id: str, **kwargs):
    e = entity(entity_id)
    _last_seen_older, _when = e.last_active_older_than(**kwargs)
    return not _last_seen_older