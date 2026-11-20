# https://github.com/custom-components/pyscript
"""Forecast of the battery of the Oktant A Invertor and advice for the generator.

Read this whole comment before you change this module.

1. PURPOSE
==========

The house battery of the Oktant A Invertor (Deye) feeds the house when the city has no power.
A generator can charge the battery, but only in its window (07:00–23:00, from the Times of Day helper
`binary_sensor.galaktyka_generator_allowed`). This module answers three questions:

- In how many hours does the battery go empty without the city power and without the generator?
- In how many hours does the city power come back?
- Is the generator necessary, what is the latest start time, and when can it stop?

The module only calculates. It never reads Home Assistant and never switches anything.
The agent must never write to the inverter or to the generator switch.

2. WHO USES THIS MODULE
=======================

- `pyscript/oktant_generator_advisor.py` reads the states, the hourly statistics and the DTEK calendar,
  calls the functions of this module, and writes the output entities. It sends the important messages to
  Telegram as a chart picture (`pyscript/modules/oktant_chart.py`) and the `debug` calculation to Discord.
  All constants (entity IDs, rates, thresholds, windows, margin) are at the top of that script.
  The script passes each number to the functions here. This module has no constants of its own,
  except the names of the states below.
- `/config/plans/oktant-generator-advisor/tests/test_forecast.py` tests this module with plain Python.
  Run: `uv run --no-project --with pytest --with pillow pytest H:/plans/oktant-generator-advisor/tests -q`
  (`H:` is `/config` over SMB). Each change of the logic needs a test there, and all tests must pass.
- The plan and the measured facts: `/config/plans/oktant-generator-advisor/`
  (`00-context.md`, `01-implementation-plan.md`).

3. RULES FOR THE CODE (pyscript runs this file through its own interpreter)
==========================================================================

- No pyscript names (`state`, `log`, `hass`, `task`, decorators). Then plain Python can import the module.
- No generator expressions, for example `any(x for x in items)`. pyscript does not run them. Use a loop.
  A list comprehension is allowed.
- No classes. pyscript gives a method only a weak reference to its instance. The battery is a dict.
- No nested functions. Write each helper at the top level.
- A save of this file reloads `oktant_generator_advisor.py` on the live HA at once, so save each change
  in one complete step, and run the tests first.

4. UNITS AND NAMES
==================

- Energy in kWh, power in kW, charge in percent, time as aware datetimes in the local time zone.
- "Usable energy" is the energy above the zero point. The zero point is
  `input_number.oktant_a_invertor_target_discharge_soc` (13 %): the inverter turns off there.
  So usable energy 0 means "the house has no power".
- "Window" is the generator window as minutes of the day: `window_start_minutes` (420 = 07:00)
  and `window_end_minutes` (1380 = 23:00). Inside the window the generator can run, and the forecast
  uses the day load. Outside the window the generator cannot run, and the forecast uses the night load.
- "Forecast end" is the next start of the window after now (`forecast_end`). Example: at 10:00 the forecast
  ends at 07:00 of the next day, at 02:00 it ends at 07:00 of the same day. After that moment the generator
  can run again, so a longer forecast is not necessary.

5. STEP 1: CITY MODE (`city_share`, `city_mode`)
================================================

`city_share` is the mean of `sensor.kyiv_groups_total_percent` and `sensor.kyiv_groups_2_total_percent`:
the share of Kyiv that has power now. Measured: 93–96 % when DTEK applies no schedule, below 92 %
(in daytime 49–80 %) when DTEK applies schedules.

`city_mode` returns `follow_schedule` or `ignore_schedule`:

- share >= `ignore_from_percent` (90): `ignore_schedule`. DTEK applies no schedule now,
  so the future outages of the calendar do not occur.
- share < `follow_below_percent` (85): `follow_schedule`.
- between the two values: the previous mode stays. This stops a change back and forth each few minutes.
  The script keeps the previous mode in `pyscript.oktant_a_invertor_generator_advisor_memory`.
- no share: the previous mode, else `follow_schedule`.

A low share alone does not mean an emergency (12.11 at 49 % DTEK showed `planned_outage`).
Only `sensor.dtek_electricity` = `emergency` means an emergency.

6. STEP 2: FORECAST OF THE CITY POWER (`grid_forecast`)
=======================================================

Input `grid_on`: the script sets it when `input_boolean.power` or `input_boolean.power_2_line` or
`binary_sensor.oktant_a_invertor_grid` is `on`. The inverter has city power from either input.

The result has `mode`, `off_intervals` (list of (start, end) without city power, cut at the forecast end),
`expected_at` (None when unknown), `hours_until` and `at_least` (True: the power can come later than
`expected_at`/`hours_until` say, because the forecast ends there).

| Situation                                        | mode            | off_intervals                                  |
|--------------------------------------------------|-----------------|------------------------------------------------|
| grid_on                                          | `on`            | calendar outages after now, only in follow_schedule |
| dtek `planned_outage`, next_connectivity > now   | `schedule`      | [now, next_connectivity] + later calendar outages (follow_schedule) |
| dtek `planned_outage`, no known end              | `default_hours` | [now, now + optimistic_outage_hours] + later outages (follow_schedule) |
| not `emergency`, less than `grace_minutes` after `planned_end` | `late` | [now, planned_end + grace] + later outages (follow_schedule) |
| dtek `emergency`, `normal` (outage outside the schedule), or any other state | `pessimistic` | [now, forecast end] |

The `late` mode never hides an urgent advice: the script also runs the pessimistic forecast, and when its
advice is urgent (`is_urgent`: start_now or outside_hours), the script uses the pessimistic one.

The decision of the user: an emergency or an unknown outage is pessimistic, a planned outage without a known
end is optimistic (a constant number of hours, counted from now).

The script passes the calendar through `schedule_outages` first. It drops each event longer than
`DTEK_OUTAGE_MAX_HOURS`: DTEK marks an emergency regime with one event for whole days, and with the grid on
that event made the forecast count the whole night without power (2026-11-20).

7. STEP 3: BATTERY FORECAST (`make_battery`, `simulate`, `hours_until_empty`)
=============================================================================

`make_battery` turns the inputs into a dict: total size (capacity Ah x voltage V / 1000), usable energy now,
usable maximum (100 % minus the zero point), day and night load, and the charge rates in kW.
The rates come in percent per hour of the total size: the city grid 11 %/h, the generator 12 %/h (measured).
The day load is the mean of the hourly means of the window hours of the last 7 days, the night load
the same for the hours outside the window of the last 7 nights (decision of the user).

`simulate` walks from now to the forecast end in steps (15 minutes). In each step exactly one of these applies:

- city power (the step is not in `off_intervals`): + grid rate. The load takes nothing from the battery.
- generator: + generator rate. The load takes nothing from the battery. The generator runs only when all are
  true: the step is at or after `generator_start`, before `generator_stop` (None = no stop), in the window,
  and without city power.
- else: - load of the step (day or night load by the window).

The usable energy never goes above the usable maximum. At the maximum a running generator stays on and
only feeds the load. This matters: it makes "an earlier start is never worse" true, and the binary
searches in step 4 depend on it. Do not add "stop when full" without a change of the searches.

`simulate` returns `min_kwh` (the lowest usable energy), `empty_at` (first step below zero) and `points`.

`hours_until_empty` ignores the city power and the generator and counts until the usable energy is zero,
up to `max_hours`. It is the value of `sensor.oktant_a_invertor_battery_hours_left`.

8. STEP 4: GENERATOR (`latest_start`, `earliest_stop`, `generator_run_end`)
===========================================================================

- Start candidates: each step in the window and without city power.
- `latest_start`: the last candidate from which a generator without a stop keeps `min_kwh >= 0`.
  Binary search, because an earlier start never gives less energy. None: even the first candidate fails.
- `earliest_stop`: for a given start, the first step at which the generator can stop and the battery still
  keeps `min_kwh >= 0`. Binary search, because a later stop never gives less energy. None: no stop works.
- `generator_run_end`: a stop, but not after the end of the window.

9. STEP 5: ADVICE (`advise`)
============================

`advise` runs `simulate` without the generator first. `deficit_kwh` = -min_kwh when it is below zero.
The state, in this order of checks:

1. `running`: the generator runs now. `stop_at` = `earliest_stop` from now. If no stop works,
   `enough` = False and `stop_at` = the end of the window.
2. `not_needed`: no deficit.
3. `outside_hours`: a deficit, but the window is closed now (`binary_sensor.galaktyka_generator_allowed` off).
4. No `latest_start`:
   - the city power is on now: `not_needed` with `night_risk` = True. The generator cannot help, because the
     outage comes when the generator cannot run. The reason text warns.
   - else `start_now` with `enough` = False: even a start now cannot fill the whole deficit.
5. `start_now`: now >= latest_start - `start_margin_minutes` (30). The margin is the time for a person to go
   and start the generator, not a charge time.
6. `needed_later`: the generator is necessary, but there is time until the latest start.

For states 4–6, `stop_at` and `generator_hours_needed` describe the run from the latest start (or from now).

`binary_sensor.oktant_a_invertor_generator_start_now` is `on` only in `start_now`. The user connects it to the
generator switch in an own automation.

10. STEP 6: TEXT (`reason_text`, `hhmm`)
========================================

`reason_text` gives one sentence in Ukrainian for the attribute `reason` and for Discord. Keep it short
and plain. A new advice state needs a new sentence here and a test.

11. HOW TO CHANGE THE LOGIC
===========================

1. Read sections 5–9 and find the step that the change touches.
2. Write a test in `tests/test_forecast.py` with real numbers (battery 167 kWh, zero 13 %, day 14 kW,
   night 9 kW, grid 11 %/h, generator 12 %/h, window 07:00–23:00, step 15 min). Calculate the expected
   value by hand in a comment.
3. Change the code. Keep the rules of section 3.
4. Run all tests. Then save the file and read the live outputs and the system log of HA.
5. A new input or constant goes to the top of `oktant_generator_advisor.py`, and the script passes it in.
6. Update this comment, so that it describes the new logic.
"""

from datetime import timedelta

CITY_MODE_FOLLOW = 'follow_schedule'
CITY_MODE_IGNORE = 'ignore_schedule'

GRID_MODE_ON = 'on'
GRID_MODE_SCHEDULE = 'schedule'
GRID_MODE_DEFAULT_HOURS = 'default_hours'
GRID_MODE_PESSIMISTIC = 'pessimistic'
GRID_MODE_LATE = 'late'

ADVICE_NOT_NEEDED = 'not_needed'
ADVICE_NEEDED_LATER = 'needed_later'
ADVICE_START_NOW = 'start_now'
ADVICE_RUNNING = 'running'
ADVICE_OUTSIDE_HOURS = 'outside_hours'
ADVICE_UNAVAILABLE = 'unavailable'

DTEK_NORMAL = 'normal'
DTEK_PLANNED = 'planned_outage'
DTEK_EMERGENCY = 'emergency'


def to_float(value):
    """Return a float, or None for a value that is not a number."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def city_share(percent_1, percent_2):
    """Mean share of Kyiv with power, or None when no value is a number."""
    values = []
    for value in [to_float(percent_1), to_float(percent_2)]:
        if value is not None:
            values.append(value)
    if not values:
        return None
    return sum(values) / len(values)


def city_mode(share, previous_mode, ignore_from_percent, follow_below_percent):
    """Tell if DTEK applies its schedule now.

    At `ignore_from_percent` and more, DTEK applies no schedule. Below `follow_below_percent`, it does.
    Between the two values, the mode stays as it was, so that it does not change back and forth.
    """
    if share is None:
        return previous_mode or CITY_MODE_FOLLOW
    if share >= ignore_from_percent:
        return CITY_MODE_IGNORE
    if share < follow_below_percent:
        return CITY_MODE_FOLLOW
    return previous_mode or CITY_MODE_FOLLOW


def minutes_of_day(moment):
    return moment.hour * 60 + moment.minute


def in_window(moment, window_start_minutes, window_end_minutes):
    """True when the time of day of `moment` is in [start, end)."""
    minute = minutes_of_day(moment)
    if window_start_minutes <= window_end_minutes:
        return window_start_minutes <= minute < window_end_minutes
    return minute >= window_start_minutes or minute < window_end_minutes


def next_time_of_day(now, minutes):
    """The next moment strictly after `now` with this time of day."""
    candidate = now.replace(
        hour=minutes // 60, minute=minutes % 60, second=0, microsecond=0
    )
    if candidate <= now:
        candidate = candidate + timedelta(days=1)
    return candidate


def forecast_end(now, window_start_minutes):
    """The forecast ends when the generator can run again: the next start of the window."""
    return next_time_of_day(now, window_start_minutes)


def schedule_outages(outages, max_hours):
    """The calendar outages of the hourly schedule: drop each event longer than `max_hours`.

    In an emergency, DTEK puts one event on the calendar for whole days (2026-11-20: "Emergency Outage",
    20-22 Nov). That event marks the emergency regime, not an outage of the schedule: the power can be on.
    """
    found = []
    for start, stop in outages:
        if (stop - start).total_seconds() <= max_hours * 3600:
            found.append((start, stop))
    return found


def _future_outages(outages, after, end, follow):
    """The calendar outages after `after`, cut at `end`. None of them when DTEK applies no schedule."""
    found = []
    if not follow:
        return found
    for start, stop in outages:
        if stop > after and start < end:
            found.append((max(after, start), min(end, stop)))
    return found


def grid_forecast(
    now,
    grid_on,
    dtek_state,
    next_connectivity,
    outages,
    mode_of_city,
    end,
    optimistic_outage_hours,
    planned_end=None,
    grace_minutes=0,
):
    """Forecast of the city power from now to `end`.

    `outages` is a list of (start, end) pairs from the DTEK calendar.
    `planned_end` is the end of the last planned outage (the script keeps it in its memory), `grace_minutes`
    the time after it during which a late power is still expected.
    Returns a dict: `mode`, `off_intervals` (list of (start, end)), `expected_at` (None when unknown), `hours_until`, `at_least`.
    """
    follow = mode_of_city == CITY_MODE_FOLLOW
    off_intervals = []

    if grid_on:
        off_intervals = _future_outages(outages, now, end, follow)
        return {
            'mode': GRID_MODE_ON,
            'off_intervals': off_intervals,
            'expected_at': now,
            'hours_until': 0.0,
            'at_least': False,
        }

    if dtek_state == DTEK_PLANNED:
        if next_connectivity is not None and next_connectivity > now:
            back_at = min(end, next_connectivity)
            off_intervals = [(now, back_at)] + _future_outages(
                outages, back_at, end, follow
            )
            mode = GRID_MODE_SCHEDULE
        else:
            back_at = now + timedelta(hours=optimistic_outage_hours)
            back_at = min(back_at, end)
            off_intervals = [(now, back_at)] + _future_outages(
                outages, back_at, end, follow
            )
            mode = GRID_MODE_DEFAULT_HOURS
        at_least = back_at >= end
        return {
            'mode': mode,
            'off_intervals': off_intervals,
            'expected_at': None if at_least else back_at,
            'hours_until': (back_at - now).total_seconds() / 3600,
            'at_least': at_least,
        }

    # The planned outage ended, DTEK left `planned_outage`, but the power is late (2026-11-20: end 07:30, power 08:12).
    # During the grace time the power is still expected at the end of the grace.
    if (
        dtek_state != DTEK_EMERGENCY
        and planned_end is not None
        and planned_end <= now < planned_end + timedelta(minutes=grace_minutes)
    ):
        back_at = min(end, planned_end + timedelta(minutes=grace_minutes))
        off_intervals = [(now, back_at)] + _future_outages(
            outages, back_at, end, follow
        )
        at_least = back_at >= end
        return {
            'mode': GRID_MODE_LATE,
            'off_intervals': off_intervals,
            'expected_at': None if at_least else back_at,
            'hours_until': (back_at - now).total_seconds() / 3600,
            'at_least': at_least,
        }

    # `emergency`, or no power while DTEK shows `normal` (an outage outside the schedule), or an unknown state.
    return {
        'mode': GRID_MODE_PESSIMISTIC,
        'off_intervals': [(now, end)],
        'expected_at': None,
        'hours_until': (end - now).total_seconds() / 3600,
        'at_least': True,
    }


def is_off(moment, off_intervals):
    for start, stop in off_intervals:
        if start <= moment < stop:
            return True
    return False


def make_battery(
    capacity_kwh,
    zero_percent,
    charge_percent,
    load_day_kw,
    load_night_kw,
    grid_charge_percent_per_hour,
    generator_charge_percent_per_hour,
    window_start_minutes,
    window_end_minutes,
    step_minutes,
):
    """Numbers of the battery and of the load, as a dict. All energy is usable energy above the zero point.

    A dict and not a class: pyscript gives a method only a weak reference to its instance.
    """
    return {
        'capacity_kwh': capacity_kwh,
        'zero_percent': zero_percent,
        'usable_now_kwh': capacity_kwh * (charge_percent - zero_percent) / 100,
        'usable_max_kwh': capacity_kwh * (100 - zero_percent) / 100,
        'load_day_kw': load_day_kw,
        'load_night_kw': load_night_kw,
        'grid_charge_kw': capacity_kwh * grid_charge_percent_per_hour / 100,
        'generator_charge_kw': capacity_kwh * generator_charge_percent_per_hour / 100,
        'window_start_minutes': window_start_minutes,
        'window_end_minutes': window_end_minutes,
        'step': timedelta(minutes=step_minutes),
        'step_hours': step_minutes / 60,
    }


def load_kw(battery, moment):
    if in_window(
        moment, battery['window_start_minutes'], battery['window_end_minutes']
    ):
        return battery['load_day_kw']
    return battery['load_night_kw']


def generator_allowed(battery, moment):
    return in_window(
        moment, battery['window_start_minutes'], battery['window_end_minutes']
    )


def simulate(
    battery, now, end, off_intervals, generator_start=None, generator_stop=None
):
    """Run the forecast in steps from now to `end`.

    The generator runs from `generator_start` to `generator_stop` (None: no stop), only in its window and only while the city power is off.
    While the city power or the generator runs, the load takes nothing from the battery.
    Returns a dict: `min_kwh`, `empty_at` (first moment below zero, or None), `points` (list of (moment, usable kWh)).
    """
    usable = battery['usable_now_kwh']
    lowest = usable
    empty_at = None
    points = [(now, usable)]
    moment = now
    while moment < end:
        grid = not is_off(moment, off_intervals)
        generator = (
            generator_start is not None
            and moment >= generator_start
            and (generator_stop is None or moment < generator_stop)
            and not grid
            and generator_allowed(battery, moment)
        )
        if grid:
            usable = usable + battery['grid_charge_kw'] * battery['step_hours']
        elif generator:
            usable = usable + battery['generator_charge_kw'] * battery['step_hours']
        else:
            usable = usable - load_kw(battery, moment) * battery['step_hours']
        usable = min(usable, battery['usable_max_kwh'])
        moment = moment + battery['step']
        points.append((moment, usable))
        lowest = min(lowest, usable)
        if usable < 0 and empty_at is None:
            empty_at = moment
    return {'min_kwh': lowest, 'empty_at': empty_at, 'points': points}


def hours_until_empty(battery, now, max_hours):
    """Hours until the battery is empty without the city power and without the generator."""
    usable = battery['usable_now_kwh']
    if usable <= 0:
        return 0.0, now
    moment = now
    limit = now + timedelta(hours=max_hours)
    while moment < limit:
        drain = load_kw(battery, moment) * battery['step_hours']
        if drain >= usable:
            empty_at = moment + timedelta(hours=battery['step_hours'] * usable / drain)
            return (empty_at - now).total_seconds() / 3600, empty_at
        usable = usable - drain
        moment = moment + battery['step']
    return float(max_hours), None


def _start_candidates(battery, now, end, off_intervals):
    """Each step where the generator can start: in its window and without the city power."""
    found = []
    moment = now
    while moment < end:
        if generator_allowed(battery, moment) and is_off(moment, off_intervals):
            found.append(moment)
        moment = moment + battery['step']
    return found


def _enough(battery, now, end, off_intervals, start, stop=None):
    return simulate(battery, now, end, off_intervals, start, stop)['min_kwh'] >= 0


def latest_start(battery, now, end, off_intervals):
    """The last step from which a generator that runs to the end of its window keeps the battery above zero.

    An earlier start never gives less energy, so a binary search over the candidates works.
    Returns None when even the first candidate is not enough.
    """
    candidates = _start_candidates(battery, now, end, off_intervals)
    if not candidates or not _enough(battery, now, end, off_intervals, candidates[0]):
        return None
    low = 0
    high = len(candidates) - 1
    while low < high:
        middle = (low + high + 1) // 2
        if _enough(battery, now, end, off_intervals, candidates[middle]):
            low = middle
        else:
            high = middle - 1
    return candidates[low]


def earliest_stop(battery, now, end, off_intervals, start):
    """The first step at which a generator that started at `start` can stop. None when no stop is enough."""
    stops = []
    moment = start + battery['step']
    while moment <= end:
        stops.append(moment)
        moment = moment + battery['step']
    if not stops or not _enough(battery, now, end, off_intervals, start, stops[-1]):
        return None
    low = 0
    high = len(stops) - 1
    while low < high:
        middle = (low + high) // 2
        if _enough(battery, now, end, off_intervals, start, stops[middle]):
            high = middle
        else:
            low = middle + 1
    return stops[low]


def generator_run_end(battery, start, stop):
    """The last moment of a run: `stop`, but not after the end of the generator window."""
    window_end = next_time_of_day(start, battery['window_end_minutes'])
    if stop is None or stop > window_end:
        return window_end
    return stop


def advise(
    battery,
    now,
    end,
    grid,
    generator_running,
    generator_allowed_now,
    start_margin_minutes,
):
    """Advice for the generator. `grid` is the result of `grid_forecast`."""
    off_intervals = grid['off_intervals']
    base = simulate(battery, now, end, off_intervals)
    deficit = -base['min_kwh'] if base['min_kwh'] < 0 else 0.0
    result = {
        'state': ADVICE_NOT_NEEDED,
        'deficit_kwh': round(deficit, 1),
        'empty_at': base['empty_at'],
        'latest_start': None,
        'stop_at': None,
        'generator_hours_needed': 0.0,
        'enough': True,
        'night_risk': False,
    }

    if generator_running:
        stop = earliest_stop(battery, now, end, off_intervals, now)
        result['state'] = ADVICE_RUNNING
        if stop is None:
            result['enough'] = False
            stop = generator_run_end(battery, now, None)
        result['stop_at'] = stop
        result['generator_hours_needed'] = round((stop - now).total_seconds() / 3600, 2)
        return result

    if deficit <= 0:
        return result

    if not generator_allowed_now:
        result['state'] = ADVICE_OUTSIDE_HOURS
        return result

    start = latest_start(battery, now, end, off_intervals)
    if start is None:
        if grid['mode'] == GRID_MODE_ON and not is_off(now, off_intervals):
            # The generator cannot help: the city power is on now, and the outage comes when the generator cannot run.
            result['night_risk'] = True
            return result
        result['state'] = ADVICE_START_NOW
        result['enough'] = False
        result['latest_start'] = now
        stop = generator_run_end(battery, now, None)
        result['stop_at'] = stop
        result['generator_hours_needed'] = round((stop - now).total_seconds() / 3600, 2)
        return result

    stop = earliest_stop(battery, now, end, off_intervals, start)
    stop = generator_run_end(battery, start, stop)
    result['latest_start'] = start
    result['stop_at'] = stop
    result['generator_hours_needed'] = round((stop - start).total_seconds() / 3600, 2)
    if now >= start - timedelta(minutes=start_margin_minutes):
        result['state'] = ADVICE_START_NOW
    else:
        result['state'] = ADVICE_NEEDED_LATER
    return result


def is_urgent(advice):
    """True when the advice cannot wait: start the generator now, or the battery can go empty in the night."""
    return advice['state'] in (ADVICE_START_NOW, ADVICE_OUTSIDE_HOURS)


def is_repeat(
    state,
    latest_start,
    now,
    sent_state,
    sent_latest_start,
    sent_at,
    repeat_minutes,
    shift_minutes,
):
    """True when the advice repeats the one sent not long ago, so Telegram does not get it again.

    2026-11-20: a short blip of the city power made the advice `needed_later` -> `not_needed` -> `needed_later`,
    and the script sent the same advice twice in 28 minutes. A repeat has the same state, came less than
    `repeat_minutes` after the last message, and its latest start moved by less than `shift_minutes`.
    """
    if not sent_state or state != sent_state or sent_at is None:
        return False
    if now - sent_at >= timedelta(minutes=repeat_minutes):
        return False
    if latest_start is None or sent_latest_start is None:
        return latest_start is None and sent_latest_start is None
    shift = abs((latest_start - sent_latest_start).total_seconds())
    return shift < shift_minutes * 60


def hhmm(moment):
    if moment is None:
        return '—'
    return moment.strftime('%H:%M')


def reason_text(advice, grid):
    """One sentence in Ukrainian for the attribute `reason` and for Discord."""
    state = advice['state']
    if state == ADVICE_UNAVAILABLE:
        return 'Немає вхідних даних.'
    if state == ADVICE_RUNNING:
        if not advice['enough']:
            return f"Генератор працює, але до {hhmm(advice['stop_at'])} не закриє всю нестачу."
        return f"Генератор працює. Його можна вимкнути о {hhmm(advice['stop_at'])}."
    if state == ADVICE_OUTSIDE_HOURS:
        return f"Батарея сяде о {hhmm(advice['empty_at'])}, але зараз генератор запускати не можна."
    if state == ADVICE_START_NOW:
        if not advice['enough']:
            return f"Вмикай генератор зараз. Навіть до {hhmm(advice['stop_at'])} він не закриє всю нестачу {advice['deficit_kwh']} кВт·год."
        return f"Вмикай генератор зараз, приблизно на {advice['generator_hours_needed']} год. Крайній старт {hhmm(advice['latest_start'])}."
    if state == ADVICE_NEEDED_LATER:
        return f"Генератор знадобиться: нестача {advice['deficit_kwh']} кВт·год. Крайній старт {hhmm(advice['latest_start'])}, потрібно {advice['generator_hours_needed']} год."
    if advice['night_risk']:
        return f"Світло є, але батарея може сісти о {hhmm(advice['empty_at'])}, коли генератор запускати не можна."
    return 'Генератор не потрібен.'
