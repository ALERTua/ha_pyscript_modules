import requests
from imports import *

KEY_TOKEN = 'X-CSRF-TOKEN'
KEY_SESSION_ID = 'beaker.session.id'


class Router:  # Edgerouter
    def __init__(self):
        self.session = requests.Session()
        self.url = constants.ROUTER_URL
        self.username = constants.ROUTER_USERNAME
        self.password = constants.ROUTER_PASSWORD
        self.data = {
            'username': self.username,
            'password': self.password,
        }
        self.headers = {
            'Content-type': 'application/json',
        }
        self.cookies = {}
        self.token = None

    def login(self):
        url = self.url
        data = self.data
        session = self.session
        response = task.executor(session.post, url=url, data=data, verify=False, timeout=5)
        if not response.ok:
            log.error("Router reboot not ok")
            return False

        token = session.cookies[KEY_TOKEN]
        self.headers[KEY_TOKEN] = token
        session_id = session.cookies[KEY_SESSION_ID]
        self.cookies[KEY_SESSION_ID] = session_id
        return True

    def reboot(self):
        log.info("Rebooting router")
        url = self.url
        session = self.session
        headers = self.headers
        cookies = self.cookies
        try:
            task.executor(session.post, f"{url}/api/edge/operation/reboot.json", headers=headers, cookies=cookies,
                          verify=False)
        except Exception as e:
            log.error(f"Error rebooting router via API: {type(e)} {e}")
