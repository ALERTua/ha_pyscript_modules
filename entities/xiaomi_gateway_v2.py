# https://github.com/custom-components/pyscript
from imports_base import *

"""
- "0 - Police car 1"
- "1 - Police car 2"
- "2 - Accident"
- "3 - Countdown"
- "4 - Ghost"
- "5 - Sniper rifle"
- "6 - Battle"
- "7 - Air raid"
- "8 - Bark"
#      - "9 - None"
- "10 - Doorbell"
- "11 - Knock at a door"
- "12 - Amuse"
- "13 - Alarm clock"
#      - "14 - None"
#      - "15 - None"
#      - "16 - None"
#      - "17 - None"
#      - "18 - None"
#      - "19 - None"
- "20 - MiMix"
- "21 - Enthusiastic"
- "22 - GuitarClassic"
- "23 - IceWorldPiano"
- "24 - LeisureTime"
- "25 - ChildHood"
- "26 - MorningStreamLiet"
- "27 - MusicBox"
- "28 - Orange"
- "29 - Thinker"
"""


class XiaomiGatewayV2:
    # noinspection PyMissingConstructor
    def __init__(self, mac):
        self.mac = mac

    def play_ringtone(self, id_, volume):
        mac = self.mac
        xiaomi_aqara.play_ringtone(gw_mac=mac, ringtone_id=id_, ringtone_vol=volume)

    def media_stop(self):
        mac = self.mac
        xiaomi_aqara.stop_ringtone(gw_mac=mac)
