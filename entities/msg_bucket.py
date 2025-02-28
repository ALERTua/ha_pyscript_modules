# https://github.com/custom-components/pyscript
from imports_base import *
import common_tools as tools
from entities.ha import HA

ha = HA()


class MsgBucket:
    def __init__(self, *args, **kwargs):
        self._init_(*args, **kwargs)

    def _init_(self, name=None, separator='\n', debug=False, *args, **kwargs):
        self.name = name or self.__class__.__name__
        self.msgs = []
        self.separator = separator
        self.args = args
        self.kwargs = kwargs
        self.debug = debug

    def add(self, msg, debug=False):
        if self.debug or debug:
            # log.debug(f"Adding msg to {self.__class__.__name__}: {msg}")
            log.debug(msg)
        self.msgs.append(msg)

    def _str(self):
        output = ''
        first = True
        for msg in self.msgs:
            if first:
                msg_str = f"{msg}"
                first = False
            else:
                msg_str = f"{self.separator}{msg}"
            output += msg_str
        return output

    def _send(self):
        raise NotImplementedError

    def send(self):
        if self.msgs:
            if self.debug:
                log.debug(f"{self.name}: Sending msg:\n{self._str()}")
            self._send()


class TelegramMsgBucket(MsgBucket):
    # noinspection PyMissingConstructor
    def __init__(self, *args, **kwargs):
        self._init_(*args, **kwargs)

    def _send(self):
        tools.telegram_message(msg=self._str(), *self.args, **self.kwargs)


class DiscordMsgBucket(MsgBucket):
    # noinspection PyMissingConstructor
    def __init__(self, *args, **kwargs):
        self._init_(*args, **kwargs)

    def _send(self):
        dt_str = tools.dt_to_datetime_string()
        msg = f"{dt_str}\n{self._str()}"
        # log.debug(f"sending {self.__class__.__name__} with args: {self.args}, kwargs: {self.kwargs}")
        tools.discord_message(msg=msg, *self.args, **self.kwargs)


# @time_trigger  # test
# noinspection PyUnusedLocal
def __msgbucket_test(trigger_type=None, var_name=None, value=None, old_value=None, context=None, **kwargs):
    bucket = DiscordMsgBucket()
    bucket.add('msgbucket_test')
    bucket.send()
