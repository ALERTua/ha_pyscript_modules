import common_tools as tools
import constants
from telegram_callback import register_telegram_callback
from imports_base import *
from entities.entity import entity
from entities.ha import HA
from entities.msg_bucket import MsgBucket, DiscordMsgBucket
from homeassistant.const import EVENT_CALL_SERVICE
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/template.py
import homeassistant.helpers.template as template
# https://github.com/home-assistant/core/blob/master/homeassistant/helpers/entity.py
import homeassistant.helpers.entity as entity_helper
