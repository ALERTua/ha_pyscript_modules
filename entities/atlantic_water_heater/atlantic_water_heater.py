import logging

from imports import *
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.client import OverkizClient
from pyoverkiz.enums import Server, OverkizState, OverkizCommand
from pyoverkiz.models import Command


USERNAME = "username"
PASSWORD = "password"
DEVICE_URL = 'device_url'


class AtlanticWaterHeater:
    def __init__(self, username=USERNAME, password=PASSWORD, server=SUPPORTED_SERVERS[Server.ATLANTIC_COZYTOUCH],
                 device_url=DEVICE_URL):
        self.username = username
        self.password = password
        self.server = server
        self._client: Optional[OverkizClient] = None
        self.device_url = device_url

    def client(self):
        if self._client is None or self._client.session.closed:
            log.debug("Starting Overkiz session")
            self._client = OverkizClient(self.username, self.password, server=self.server)
            result = self._client.login()
            log.debug(f"Overkiz session result: {result}")
        return self._client

    def close(self):
        if self._client is not None and not self._client.session.closed:
            log.debug("Closing Overkiz session")
            self._client.session.close()

    def execute_command(self, cmd):
        log.debug(f"Executing Overkiz command {cmd}")
        result = self.client().execute_command(self.device_url, cmd)
        log.debug(f"Overkiz command result: {result}")
        self.close()
        return result

    def set_showers(self, quantity: int):
        cmd = Command(OverkizCommand.SET_EXPECTED_NUMBER_OF_SHOWER, [quantity])
        return self.execute_command(cmd)

    def set_boost_mode(self, value: bool):
        value = 'on' if bool else 'off'
        cmd = Command(OverkizCommand.SET_BOOST_MODE, [value])
        return self.execute_command(cmd)

    def refresh_boost_mode(self):
        cmd = Command('refreshBoostMode')
        return self.execute_command(cmd)

    def state(self):
        return self.client().get_state(self.device_url)
