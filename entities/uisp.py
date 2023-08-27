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


def router_link_speed():
    uisp = UISP()
    gateways = uisp.list_gateways()
    if not gateways:
        return

    gateway_ = gateways[0]
    gateway_id = gateway_.get('id')
    gateway_info = uisp.get_gateway(gateway_id)
    return gateway_info


class UISP:  # https://192.168.1.6/nms/api-docs/
    def __init__(self):
        self.session = requests.Session()
        self.uisp_url = constants.UISP_URL
        self.url = f"{self.uisp_url}/nms/api/v2.1"
        self.token = constants.UISP_TOKEN
        self.headers = {
            'accept': 'application/json',
            'x-auth-token': self.token,
        }

    def _request(self, arg):
        url = self.url
        session = self.session
        headers = self.headers
        full_url = f"{url}/{arg}"
        log.debug(f"UISP request {full_url}")
        response = task.executor(
            session.get,
            full_url,
            headers=headers,
            verify=False
        )
        if not response.ok:
            log.warning(f"UISP request {arg} failed: {response.code} {response.reason}")
            return

        return response.json()

    def _list_devices(self, arg=''):
        full_url = f"devices{arg}"
        return self._request(full_url)

    def get_gateway(self, id_):
        """
        {'connectivityDownlinkCapacity': 1000000000,
        'connectivityIpQueue': {'clientsDownloadSpeedSum': None,
                                'clientsUploadSpeedSum': None,
                                'downloadSpeed': None,
                                'interfaceId': 'eth1',
                                'uploadSpeed': None},
        'connectivityProvider': None,
        'connectivityUplinkCapacity': 1000000000,
        'defaultIpQueue': {'downloadSpeed': None,
                            'enabled': False,
                            'uploadSpeed': None},
        'device': {'category': 'wired',
                    'features': {'isUdapiSpeedTestSupported': True},
                    'firmwareVersion': '2.0.9-hotfix.7',
                    'id': '30de5e76-f3cb-4c56-b17d-5c0ecd3eeaab',
                    'ipAddress': '192.168.1.1',
                    'mac': 'f4:92:bf:ad:2e:68',
                    'model': 'ER-X',
                    'name': 'router',
                    'platformId': 'e50',
                    'status': 'active',
                    'type': 'erouter'},
        'id': '4f6854a5-f254-4f4f-b3d5-53bd5a327d4a',
        'lastTrafficSeen': None,
        'netflowAlerts': True,
        'netflowEnabled': False,
        'netflowStatus': 'inactive',
        'qosEnabled': False,
        'statistics': {'lastSpeedtestServer': None},
        'suspend': False,
        'suspendAllowedIps': None}
        """
        return self.list_gateways(f'/{id_}')

    def list_gateways(self, arg=''):
        return self._request(f'gateways{arg}')

    def list_devices(self, type_, role):
        arg = f'?withInterfaces=true&authorized=true&type={type_}&role={role}'
        return self._list_devices(arg)

    def list_switches(self):
        return self.list_devices('eswitch', 'switch')

    def list_routers(self):
        return self.list_devices('erouter', 'router')

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



