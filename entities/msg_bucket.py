# https://github.com/custom-components/pyscript
from imports_base import *
import common_tools as tools


class MsgBucket:
    def __init__(self, name=None, separator='\n', *args, **kwargs):
        self.name = name or self.__class__.__name__
        self.msgs = []
        self.separator = separator
        self.args = args
        self.kwargs = kwargs

    def add(self, msg):
        log.debug(f"Adding msg to {self.__class__.__name__}: {msg}")
        self.msgs.append(msg)

    def _str(self):
        output = ''
        i = 0
        for msg in self.msgs:
            i += 1
            if i == 1:
                msg_str = f"{msg}"
            else:
                msg_str = f"{self.separator}{msg}"
            output += msg_str
        return output

    def _send(self):
        raise NotImplementedError

    def send(self):
        if not self.msgs:
            log.debug(f"{self.name}: Nothing to send")
            return

        log.debug(f"{self.name}: Sending msg: {self._str()}")
        self._send()


class TelegramMsgBucket(MsgBucket):
    def __init__(self, name=None, separator='\n', *args, **kwargs):
        self.name = name or self.__class__.__name__
        self.msgs = []
        self.separator = separator
        self.args = args
        self.kwargs = kwargs

    def _send(self):
        tools.telegram_message(msg=self._str(), *self.args, **self.kwargs)



class DiscordMsgBucket(MsgBucket):
    def __init__(self, name=None, separator='\n', *args, **kwargs):
        self.name = name or self.__class__.__name__
        self.msgs = []
        self.separator = separator
        self.args = args
        self.kwargs = kwargs

    def _send(self):
        # log.debug(f"sending {self.__class__.__name__} with args: {self.args}, kwargs: {self.kwargs}")
        tools.discord_message(msg=self._str(), *self.args, **self.kwargs)
