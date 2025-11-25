# https://github.com/custom-components/pyscript
from imports import *
from entities.switch import Switch


class MediaPlayer(Switch):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def wait_idle(self, state_check_now=True, state_hold=2.0, timeout=None):
        return tools.wait_speaker_idle(self.entity_id, state_check_now=state_check_now, state_hold=state_hold,
                                       timeout=timeout)

    def volume_set(self, volume_level: float):  # 1.0
        return media_player.volume_set(entity_id=self.entity_id, volume_level=volume_level)

    def volume_up(self):
        return media_player.volume_up(entity_id=self.entity_id)

    def volume_down(self):
        return media_player.volume_down(entity_id=self.entity_id)

    def volume(self):
        return self.state(attr='volume_level', default=None) or None

    def volume_limit(self, lower=0.0, upper=1.0):
        current_volume = self.volume()
        if current_volume is None:
            return

        if current_volume < lower:
            self.volume_set(lower)
        elif current_volume > upper:
            self.volume_set(upper)

    def turn_on(self):
        if self.is_on():
            return

        homeassistant.turn_on(entity_id=self.entity_id)
        task.sleep(0.5)
        volume = self.volume()
        i = 0
        delay = 0.25
        max_i = 10 * (1 / delay)
        while volume is None:
            if i >= max_i:
                break

            volume = self.volume()
            if volume is None:
                task.sleep(delay)
                i += delay

        self.volume_set(0)
        task.sleep(0.5)
        self.volume_set(volume)

    def media_title(self):
        return self.state('media_title')

    def media_content_id(self):
        return self.state('media_content_id')

    def media_artist(self):
        return self.state('media_artist')

    def media_album_name(self):
        return self.state('media_album_name')

    def media_album_artist(self):
        return self.state('media_album_artist')

    def media_content_type(self):
        return self.state('media_content_type')  # music

    def media_app_id(self):
        return self.state('app_id')  # music_assistant

    def media_shuffle(self):
        return self.state('shuffle')

    def media_repeat(self):
        return self.state('repeat')



# # off
# {'entity_id': 'media_player.shower_speaker',
#  'state': 'off',
#  'attributes': {
#    'device_class': 'speaker',
#    'friendly_name':
#        'Shower Speaker',
#    'supported_features': "<MediaPlayerEntityFeature.PAUSE|VOLUME_SET|VOLUME_MUTE|TURN_ON|TURN_OFF|PLAY_MEDIA|STOP|PLAY|BROWSE_MEDIA: 152461>"
#  },
#  'last_changed': '2024-03-19T10:07:27.799435+00:00',
#  'last_updated': '2024-03-19T10:07:27.799435+00:00',}

# # on
# {
#     'entity_id': 'media_player.shower_speaker',
#     'state': 'idle',
#     'attributes': {
#         'volume_level': 0.3500000238418579,
#         'is_volume_muted': False,
#         'media_content_type': "<MediaType.MUSIC: 'music'>",
#         'media_position_updated_at': "datetime.datetime(2024, 3, 19, 16, 39, 40, 652720, tzinfo=datetime.timezone.utc)",
#         'app_id': 'CC1AD845',
#         'app_name': 'Default Media Receiver',
#         'entity_picture_local': None,
#         'device_class': 'speaker',
#         'friendly_name': 'Shower Speaker',
#         'supported_features': "<MediaPlayerEntityFeature.PAUSE|VOLUME_SET|VOLUME_MUTE|TURN_ON|TURN_OFF|PLAY_MEDIA|STOP|PLAY|BROWSE_MEDIA: 152461>"},
#     'last_changed': '2024-03-19T16:39:40.555070+00:00',
#     'last_updated': '2024-03-19T16:39:40.652962+00:00',
# }
