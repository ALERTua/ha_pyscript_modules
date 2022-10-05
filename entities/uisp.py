import requests
from imports import *


def restart_router_port():
    uisp = UISP()
    switches = uisp.list_switches()
    if not switches:
        return

    switch_ = switches[0]
    switch_id = switch_.get('identification', dict()).get('id')
    if not switch_id:
        return

    port_name = 'port1'
    uisp.port_reset(switch_id, port_name)


class UISP:
    def __init__(self):
        self.session = requests.Session()
        self.uisp_url = constants.UISP_URL
        self.url = f"{self.uisp_url}/nms/api/v2.1"
        self.token = constants.UISP_TOKEN
        self.headers = {
            'accept': 'application/json',
            'x-auth-token': self.token,
        }

    def list_switches(self):
        url = self.url
        session = self.session
        headers = self.headers
        full_url = f"{url}/devices?withInterfaces=true&authorized=true&type=eswitch&role=switch"
        response = task.executor(
            session.get,
            full_url,
            headers=headers,
            verify=False
        )
        if not response.ok:
            log.warning(f"UISP list_switches failed: {response.code} {response.reason}")
            return

        return response.json()

    def port_reset(self, device_id, port_name):
        log.info(f"Resetting UISP {device_id} Port {port_name}")
        url = self.url
        session = self.session
        headers = self.headers
        full_url = f"{url}/devices/{device_id}/interfaces/{port_name}/reset"
        response = task.executor(
            session.post,
            full_url,
            headers=headers,
            verify=False
        )
        if not response.ok:
            log.warning(f"UISP {device_id} Port {port_name} reset failed: {response.code} {response.reason}")
            return

        log.info(f"UISP {device_id} Port {port_name} reset")
        return response.json()



