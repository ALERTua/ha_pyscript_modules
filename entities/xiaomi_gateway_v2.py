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
    def __init__(self, mac=GATEWAY_V2_MAC):
        self.mac = mac

    def play_ringtone(self, id_, volume=1):
        mac = self.mac
        xiaomi_aqara.play_ringtone(gw_mac=mac, ringtone_id=id_, ringtone_vol=volume)

    def stop_ringtone(self):
        mac = self.mac
        xiaomi_aqara.stop_ringtone(gw_mac=mac)

    def sound_knock_knock_once(self, volume=1):
        self.play_ringtone(11, volume)
        task.sleep(1)
        self.stop_ringtone()

    def sound_no_internet_once(self, volume=1):
        self.play_ringtone(29, volume)
        task.sleep(1.2)
        self.stop_ringtone()

    def sound_clock_alarm_once(self, volume=1):
        self.play_ringtone(13, volume)
        task.sleep(2.5)
        self.stop_ringtone()

    def sound_doorbell_once(self, volume=1):
        self.play_ringtone(10, volume)
        task.sleep(1.5)
        self.stop_ringtone()

    def sound_doorbell_twice(self, volume=1):
        self.play_ringtone(10, volume)
        task.sleep(3)
        self.stop_ringtone()

    def sound_child_once(self, volume=1):
        self.play_ringtone(25, volume)
        task.sleep(3.5)
        self.stop_ringtone()

    def sound_air_raid(self, volume=1):
        self.play_ringtone(7, volume)
