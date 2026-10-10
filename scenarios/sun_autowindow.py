import math

from imports import *
from entities.window import Window
from scenarios.sun_illum_autowindow import (
    END,
    ILLUM_SWITCHES,
    RANGE,
    illum_enabled,
    is_cloudy,
    is_hot,
    number_or_none,
    state_of,
)

# HOW THE COVERS FOLLOW THE SUN
#
# Geometry
# - The windows of the bedroom, the room, the office and the kitchen are on one facade
#   of the 25-storey building at Yevhena Sverstiuka 6-A, Kyiv (OSM way 776097579).
#   Window point: 50.4455, 30.6035, about 72 m above the ground.
# - The facade faces azimuth 267.2 deg (the outward normal of the west edge of OSM way 776097579).
#   A flat wall sees the sun from 177.2 to 357.2 deg.
# - Window openings from the floor plan (opening height / sill height):
#   bedroom 2.055 m / 0.645 m, room 2.04 m / 0.66 m, office 2.055 m / 0.645 m,
#   kitchen 1.725 m / 0.975 m.
#
# Sun limits
# - AZIMUTH_LOW = 210: the sun first reaches the glass at azimuth 210 deg, which the user saw
#   on 2026-10-07 at 14:31 local time. The window reveal blocks 177..210 deg.
# - AZIMUTH_HIGH = 316: the summer sunset is at azimuth up to 309 deg. A 75 m building
#   (OSM way 161955952, 168 m away, azimuth 289..316 deg) hides the sun below 1.0 deg elevation.
# - ELEVATION_LOW = 0.5: below this elevation the covers open (decision of the user).
#
# Sun in the window sector (azimuth >= 210, elevation > 0), 15th day of the month, local time:
#   Jan 15:15..17:20 max el 13 | Apr 14:25..19:50 max el 46 | Jun 14:05..21:05 max el 60
#   Oct 14:35..18:00 max el 26 | Dec 15:05..16:50 max el 11
#
# Decision order in target_position()
#   0. The sun is before AZIMUTH_LOW: leave the cover alone.
#   1. The sun is past AZIMUTH_HIGH or below ELEVATION_LOW: open (forced), except while a
#      sunset_not_on entity is on (someone asleep).
#   2. No direct sun (sun_illum_autowindow.is_cloudy) and the light switch of the window
#      (sun_illum_autowindow.ILLUM_SWITCHES) is on: open (forced).
#   3. Hot outside (sun_illum_autowindow.is_hot): close to the limit of the window.
#   4. Otherwise the adaptive-cover formula, then the limit of the window.
# A forced decision may open a cover, and it is sent once per change of the decision, so a cover
# closed by hand stays closed. Other decisions only close a cover further, so that the cover
# does not move back and forth during the afternoon.
#
# The adaptive-cover formula (https://github.com/basbruss/adaptive-cover, AdaptiveVerticalCover)
# gives the open height of a vertical cover from the sill:
#   gamma = (window_azimuth - sun_azimuth + 180) % 360 - 180
#   open_height = clip(glare_depth / cos(gamma) * tan(elevation), 0, window_height)
#   closed_percent = 100 - open_height / window_height * 100
# glare_depth is how far direct sun may reach into the room at sill height. The user chose 0.5 m.
# The closed percentage is rounded up to POSITION_STEP (10 %) so that the cover moves rarely.
# On this facade the closed percentage only grows during the afternoon (checked for the 1st and
# the 15th of every month).
#
# Closed % with glare_depth 0.5 m and the limit of each window
# (old elevation step table -> formula before rounding):
#   Apr 15 14:30 el 45: bedroom 70->58, room 70->58, kitchen 70->50
#   Apr 15 15:30 el 39: bedroom 90->76, room 80->76, kitchen 80->71
#   Jun 15 14:30 el 58: bedroom 50->46, room 50->45, kitchen 50->35
#   Jun 15 15:30 el 50: bedroom 50->68, room 50->68, kitchen 50->62
#   Aug 15 15:30 el 43: bedroom 80->73, room 80->72, kitchen 80->67
#   Oct 15 15:30 el 21: bedroom 90->87, room 80->80, kitchen 80->80
# After about 16:30 the limit (80 or 90) decides.
#
# How to recompute
# - Sun positions: astral.sun.azimuth / astral.sun.elevation for Observer(50.4455, 30.6035, 72 m).
# - Facade azimuth and obstacles: Overpass query
#   [out:json];way(around:900,50.4455,30.6035)[building]["building:levels"];out tags geom;
#   Building height = height tag, else building:levels * 3 m. The eye height is 72 m.
#
# Files
# - This module holds the window table, the decision and the sun, pause and sunset triggers.
# - scenarios/sun_illum_autowindow.py holds the light and heat conditions, the light triggers,
#   END and RANGE.
# - pyscript/sun_autowindow.py only imports both modules, because pyscript loads a module and
#   its triggers only when a script imports it.
#
# pyscript limits met here: state.get raises NameError for a missing entity (use state_of),
# generator expressions do not run, and methods bind by weak reference (keep an instance in a
# variable before calling a method on it).

AZIMUTH_LOW = 210
AZIMUTH_HIGH = 316
ELEVATION_LOW = 0.5
WINDOW_AZIMUTH = 267.2  # outward normal of the facade
GLARE_DEPTH = 1.0  # metres of direct sun allowed into the room at sill height
POSITION_STEP = 10  # the closed percentage is rounded up to this step to move the cover rarely
POSITION_OPEN = 0

AZIMUTH = 'sun.sun.azimuth'
ELEVATION = 'sun.sun.elevation'
PAUSE_SWITCH = 'input_boolean.sun_autowindow_pause'
DISCORD_TARGET = ['1223990700266356847']
DEBUG = False
REASON_SUN_LEFT = 'the sun left the window'

# limit: max closed %; height: opening, m; not_on: skip while any is on;
# sunset_not_on: no opening at sunset while any is on; closed_window_reed: skip unless 'off';
# reed_max_silence_hours: skip when the reed sent nothing for longer.
WINDOWS = {
    'office': {
        'cover': OFFICE_WINDOW,
        'switch': 'input_boolean.sun_office_autowindow',
        'limit': 80,
        'height': 2.055,
    },
    'kitchen': {
        'cover': KITCHEN_WINDOW,
        'switch': 'input_boolean.sun_kitchen_autowindow',
        'limit': 80,
        'height': 1.725,
        'not_on': [PROJECTOR],
    },
    'bedroom': {
        'cover': BEDROOM_WINDOW,
        'switch': 'input_boolean.sun_bedroom_autowindow',
        'limit': 90,
        'height': 2.055,
        'closed_window_reed': BEDROOM_WINDOW_REED,
        'reed_max_silence_hours': 24,
        'sunset_not_on': [SOMEONE_ASLEEP],
    },
    'room': {
        'cover': ROOM_WINDOW,
        'switch': 'input_boolean.sun_room_autowindow',
        'limit': 80,
        'height': 2.04,
        'closed_window_reed': ROOM_WINDOW_REED,
    },
}

# Last forced decision sent to each cover: (position, reason)
_forced_sent = {}


def adaptive_closed_percent(azimuth, elevation, window_height, glare_depth, window_azimuth):
    """Closed percentage that lets direct sun reach at most glare_depth into the room."""
    gamma = (window_azimuth - azimuth + 180) % 360 - 180
    cos_gamma = math.cos(math.radians(gamma))
    if cos_gamma <= 0.01:
        return 0
    open_height = glare_depth / cos_gamma * math.tan(math.radians(elevation))
    open_height = min(max(open_height, 0), window_height)
    closed = 100 - open_height / window_height * 100
    return min(int(math.ceil(closed / POSITION_STEP) * POSITION_STEP), 100)


def target_position(key, azimuth, elevation):
    """Return (closed percentage, forced, reason), or None to leave the cover alone."""
    window = WINDOWS[key]
    if azimuth < AZIMUTH_LOW:
        return None
    if azimuth > AZIMUTH_HIGH or elevation < ELEVATION_LOW:
        return POSITION_OPEN, True, REASON_SUN_LEFT
    # is_cloudy() runs first, because it keeps the light hysteresis up to date for all windows
    if is_cloudy() and illum_enabled(key):
        return POSITION_OPEN, True, 'no direct sun'
    if is_hot():
        return window['limit'], False, 'hot outside'
    closed = adaptive_closed_percent(azimuth, elevation, window['height'], GLARE_DEPTH, WINDOW_AZIMUTH)
    return min(closed, window['limit']), False, 'sun formula'


def is_on(entity_id):
    return state_of(entity_id) in ('on', 'home')


def any_on(entity_ids):
    # pyscript does not run generator expressions
    for entity_id in entity_ids:
        if is_on(entity_id):
            return True
    return False


def may_move(window):
    """The switch of the window is on and its cover exists."""
    return is_on(window['switch']) and state_of(window['cover']) not in UNK_O


def window_enabled(window):
    """True when the automation may move this cover now."""
    if not may_move(window) or is_on(PAUSE_SWITCH) or any_on(window.get('not_on', [])):
        return False
    reed = window.get('closed_window_reed')
    if reed and state_of(reed) != 'off':
        return False
    silence = window.get('reed_max_silence_hours')
    if reed and silence:
        reed_entity = entity(reed)
        reed_silent, _ = reed_entity.last_active_older_than(hours=silence)
        if reed_silent:
            return False
    return True


def update_window(key):
    """Move the cover of WINDOWS[key] to the position that the sun and the light ask for."""
    window = WINDOWS[key]
    if not window_enabled(window):
        return

    sun = state.getattr('sun.sun') or {}
    azimuth = number_or_none(sun.get('azimuth'))
    elevation = number_or_none(sun.get('elevation'))
    if azimuth is None or elevation is None:
        return

    target = target_position(key, azimuth, elevation)
    if target is None:
        return
    position, forced, reason = target
    if reason == REASON_SUN_LEFT and any_on(window.get('sunset_not_on', [])):
        return

    blind = Window(window['cover'], reverse=True)
    current = number_or_none(blind.position())
    if forced:
        if _forced_sent.get(key) == (position, reason):
            return
        _forced_sent[key] = (position, reason)
    else:
        _forced_sent.pop(key, None)
        if current is not None and current >= position:
            return
    if current == position:
        return

    msg = (
        f"Azimuth: {azimuth} Elevation: {elevation}\n"
        f"{reason}: setting {blind.friendly_name()} position from {current} to {position}"
    )
    log.info(f"{__name__}:\n{msg}")
    tools.discord_message(msg, target=DISCORD_TARGET)
    blind.position_set(position)


def for_each_window(action):
    """Run action(key) for every window; one failing cover does not stop the others."""
    for key in WINDOWS:
        try:
            action(key)
        except Exception as e:
            log.error(f"{__name__}: {key}: {e!r}")


def update_all():
    for_each_window(update_window)


def open_at_sunset(key):
    window = WINDOWS[key]
    if not may_move(window):
        return
    if any_on(window.get('not_on', []) + window.get('sunset_not_on', [])):
        return
    blind = Window(window['cover'], reverse=True)
    blind.open()


def open_on_pause(key):
    window = WINDOWS[key]
    if may_move(window):
        blind = Window(window['cover'], reverse=True)
        blind.open()


@state_trigger(f"{PAUSE_SWITCH} == 'on'", state_hold=3)
def sun_autowindow_pause(**kwargs):
    log.debug("Sun AutoWindow pause: opening the covers")
    for_each_window(open_on_pause)


@time_trigger(f'once({END})', 'once(09:00)', 'once(11:00)')
@state_active(f"{PAUSE_SWITCH} == 'on'")
def sun_autowindow_pause_reset():
    log.debug("Resetting Sun AutoWindow Pause")
    input_boolean.turn_off(entity_id=PAUSE_SWITCH)


@task_unique('sun_office_autowindow', kill_me=True)
@state_trigger(AZIMUTH, ELEVATION, WINDOWS['office']['switch'], ILLUM_SWITCHES['office'], PAUSE_SWITCH)
@time_active(RANGE)
def func_sun_office_autowindow(**kwargs):
    update_window('office')


@task_unique('sun_kitchen_autowindow', kill_me=True)
@state_trigger(AZIMUTH, ELEVATION, WINDOWS['kitchen']['switch'], ILLUM_SWITCHES['kitchen'], PAUSE_SWITCH, PROJECTOR)
@time_active(RANGE)
def func_sun_kitchen_autowindow(**kwargs):
    update_window('kitchen')


@task_unique('sun_bedroom_autowindow', kill_me=True)
@state_trigger(
    AZIMUTH, ELEVATION, WINDOWS['bedroom']['switch'], ILLUM_SWITCHES['bedroom'], PAUSE_SWITCH, BEDROOM_WINDOW_REED
)
@time_active(RANGE)
def func_sun_bedroom_autowindow(**kwargs):
    update_window('bedroom')


@task_unique('sun_room_autowindow', kill_me=True)
@state_trigger(AZIMUTH, ELEVATION, WINDOWS['room']['switch'], ILLUM_SWITCHES['room'], PAUSE_SWITCH, ROOM_WINDOW_REED)
@time_active(RANGE)
def func_sun_room_autowindow(**kwargs):
    update_window('room')


@time_trigger('once(sunset)')
def sun_autowindow_open_at_sunset():
    for_each_window(open_at_sunset)


@service()
def sun_autowindow_disable(**kwargs):
    for window in WINDOWS.values():
        _switch = window['switch']
        if state_of(_switch) in ['off', *UNK_O]:
            continue
        log.info(f"Turning {_switch} off")
        input_boolean.turn_off(entity_id=_switch)
