# https://github.com/custom-components/pyscript
"""Forecast of the battery of the Oktant A Invertor and advice for the generator.

Read this whole comment before you change this module.

1. PURPOSE
==========

The house battery of the Oktant A Invertor (Deye) feeds the house when the city has no power.
A generator can charge the battery, but only in its window (08:00–22:00, from the Times of Day helper
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
- "Window" is the generator window as minutes of the day: `window_start_minutes` (480 = 08:00)
  and `window_end_minutes` (1320 = 22:00). Inside the window the generator can run, and the forecast
  uses the day load. Outside the window the generator cannot run, and the forecast uses the night load.
- "Forecast end" is the next start of the window after now (`forecast_end`). Example: at 10:00 the forecast
  ends at 08:00 of the next day, at 02:00 it ends at 08:00 of the same day. After that moment the generator
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

Input `grid_on`: the script reads `binary_sensor.oktant_a_invertor_grid`, the grid state that the inverter measures.
Only while that sensor is not `on` or `off`, it takes `input_boolean.power` (the second line) or
`input_boolean.power_1_line` (the first line).
The inverter has city power from either input.

The result has `mode`, `off_intervals` (list of (start, end) without city power, cut at the forecast end),
`expected_at` (None when unknown), `hours_until` and `at_least` (True: the power can come later than
`expected_at`/`hours_until` say, because the forecast ends there).

| Situation                                        | mode            | off_intervals                                  |
|--------------------------------------------------|-----------------|------------------------------------------------|
| grid_on                                          | `on`            | calendar outages after now, only in follow_schedule |
| dtek `planned_outage`, next_connectivity > now   | `schedule`      | [now, next_connectivity] + later calendar outages (follow_schedule) |
| dtek `planned_outage`, no known end              | `default_hours` | [now, now + optimistic_outage_hours] + later outages (follow_schedule) |
| not `emergency`, follow_schedule, a calendar outage covers now | `schedule` | [now, end of that outage] + later outages |
| not `emergency`, less than `grace_minutes` after `planned_end` | `late` | [now, planned_end + grace] + later outages (follow_schedule) |
| dtek `emergency`, `normal` (outage outside the schedule), or any other state | `pessimistic` | [now, forecast end] |

The `late` mode never hides an urgent advice: the script also runs the pessimistic forecast, and when its
advice is urgent (`is_urgent`: start_now or outside_hours), the script uses the pessimistic one.

The decision of the user: an emergency or an unknown outage is pessimistic, a planned outage without a known
end is optimistic (a constant number of hours, counted from now).

The calendar row exists because `sensor.dtek_electricity` can stay `normal` for some minutes after an outage of the
calendar starts, and DTEK itself often cuts the power 15 minutes or more after the start of the schedule.
Without the row, the first minutes of each planned outage looked like an outage outside the schedule (pessimistic).

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

The state is decided at the start of a step. A step that crosses an edge is cut there into parts: the window start
or end, the start or end of an off interval, the generator start or stop. Without the cut, a step from 22:58 to
23:13 counted 15 minutes of the generator, and the chart showed the generator line rising after 23:00.
`hours_until_empty` cuts its steps at the window edges in the same way.

The usable energy never goes above the usable maximum. At the maximum a running generator stays on and
only feeds the load. This matters: it makes "an earlier start is never worse" true, and the binary
searches in step 4 depend on it. Do not add "stop when full" without a change of the searches.

`simulate` returns `min_kwh` (the lowest usable energy), `empty_at` (first step below zero) and `points`.

`chart_lines` gives the two lines of the chart, without and with the generator, up to the forecast end. When the
city power is off at the forecast end, people start the generator as the window opens, so each line gets a morning
part in which the charge grows again (from the zero point when the line is already empty). The empty moment of a
line after the forecast end (without the morning generator) is only for the text.

`hours_until_empty` ignores the city power and the generator and counts until the usable energy is zero,
up to `max_hours`. It is the value of `sensor.oktant_a_invertor_battery_hours_left`.

8. STEP 4: GENERATOR (`latest_start`, `earliest_stop`, `generator_run_end`)
===========================================================================

- Start candidates: now and each moment of the clock grid of the step (:00, :15, :30, :45) in the window and
  without city power. Stops of `earliest_stop` use the same grid and the forecast end.
- `latest_start`: the last candidate from which a generator without a stop keeps `min_kwh >= 0`.
  Binary search, because an earlier start never gives less energy. None: even the first candidate fails.
- `earliest_stop`: for a given start, the first step at which the generator can stop and the battery still
  keeps `min_kwh >= 0`. Binary search, because a later stop never gives less energy. None: no stop works.
- `generator_run_end`: a stop, but not after the end of the window.

The texts of the chart and of its Telegram caption (`chart_headline`, `summary_lines`, `dot_notes`) are at the
end of this module, so that the chart and the caption say the same.

9. STEP 5: ADVICE (`advise`)
============================

`advise` runs `simulate` without the generator first. `deficit_kwh` = -min_kwh when it is below zero.
The state, in this order of checks:

1. `running`: the generator runs now. `stop_at` = now when the city power is on now (`stop_reason` 'grid': the
   house takes nothing from the battery, so the generator adds nothing) or when the battery lasts to the forecast
   end without more generator (`stop_reason` 'enough'). Else, when the window is closed now, `stop_at` = now with
   `stop_reason` 'window' and `enough` = False: the generator must not run outside the window, and the forecast
   gives it no charge there (without this check the end of the window was the NEXT 22:00, a day later).
   Else `stop_at` = `earliest_stop` from now, which is a moment of the clock grid after now. If no stop works,
   `enough` = False and `stop_at` = the end of the window.
   The script sends "the generator can stop" only when `stop_at` <= now, so the stop now is necessary, and
   "the generator must stop" once for 'window'.
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


def _current_outage(outages, now):
    """The calendar outage that covers now, or None."""
    for start, stop in outages:
        if start <= now < stop:
            return (start, stop)
    return None


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

    # DTEK can change its state some minutes after an outage of its calendar starts (2026-11-23: event 15:00-20:00,
    # no power at 15:13, `planned_outage` only at 15:14:59). While a calendar outage covers now, the power comes at its end.
    current = _current_outage(outages, now) if follow else None
    if dtek_state != DTEK_EMERGENCY and current is not None:
        back_at = min(end, current[1])
        off_intervals = [(now, back_at)] + _future_outages(
            outages, back_at, end, follow
        )
        at_least = back_at >= end
        return {
            'mode': GRID_MODE_SCHEDULE,
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


def _window_edges(battery, moment):
    """The next start and the next end of the generator window after `moment`."""
    return [
        next_time_of_day(moment, battery['window_start_minutes']),
        next_time_of_day(moment, battery['window_end_minutes']),
    ]


def _cuts(moment, step_end, edges):
    """The moments inside (moment, step_end) from `edges`, sorted, and then `step_end`."""
    found = []
    for edge in edges:
        if edge is not None and moment < edge < step_end and edge not in found:
            found.append(edge)
    found.sort()
    found.append(step_end)
    return found


def simulate(
    battery, now, end, off_intervals, generator_start=None, generator_stop=None
):
    """Run the forecast in steps from now to `end`.

    The generator runs from `generator_start` to `generator_stop` (None: no stop), only in its window and only while the city power is off.
    While the city power or the generator runs, the load takes nothing from the battery.
    A step that crosses an edge (the window start or end, the start or end of an outage, the generator start or stop)
    is cut at that edge, so that the generator never runs after the end of its window.
    Returns a dict: `min_kwh`, `empty_at` (first moment below zero, or None), `points` (list of (moment, usable kWh)).
    """
    usable = battery['usable_now_kwh']
    lowest = usable
    empty_at = None
    points = [(now, usable)]
    fixed_edges = [generator_start, generator_stop]
    for start, stop in off_intervals:
        fixed_edges.append(start)
        fixed_edges.append(stop)
    moment = now
    while moment < end:
        step_end = min(end, moment + battery['step'])
        for cut in _cuts(
            moment, step_end, fixed_edges + _window_edges(battery, moment)
        ):
            hours = (cut - moment).total_seconds() / 3600
            grid = not is_off(moment, off_intervals)
            generator = (
                generator_start is not None
                and moment >= generator_start
                and (generator_stop is None or moment < generator_stop)
                and not grid
                and generator_allowed(battery, moment)
            )
            if grid:
                usable = usable + battery['grid_charge_kw'] * hours
            elif generator:
                usable = usable + battery['generator_charge_kw'] * hours
            else:
                usable = usable - load_kw(battery, moment) * hours
            usable = min(usable, battery['usable_max_kwh'])
            moment = cut
            points.append((moment, usable))
            lowest = min(lowest, usable)
            if usable < 0 and empty_at is None:
                empty_at = moment
    return {'min_kwh': lowest, 'empty_at': empty_at, 'points': points}


def hour_after(moment, minutes):
    """The first whole hour at least `minutes` after `moment`."""
    edge = moment + timedelta(minutes=minutes)
    right = edge.replace(minute=0, second=0, microsecond=0)
    if right < edge:
        right = right + timedelta(hours=1)
    return right


def chart_lines(
    battery,
    now,
    end,
    off_intervals,
    generator_start,
    generator_stop,
    max_hours,
    morning_hours,
):
    """The two lines of the chart: without the generator, and with the generator from `generator_start`.

    Each line goes to `end`, the start of the generator window in the morning. When the city power is off at `end`,
    people start the generator at `end`: each line gets a `morning` part from `end` for `morning_hours`, in which
    the charge grows with the generator from the charge at `end` (from the zero point when the line is already
    empty), and the right edge of the chart is `end` + `morning_hours`. Without the morning part the right edge is
    `end`.
    `empty_at` of a line is the first moment below zero without a generator after `end` (the power stays off up to
    `max_hours` after `end`), so the text can tell when the battery goes empty if nobody starts the generator in
    the morning. A moment after `end` has no dot on the chart.
    Returns a dict: `base` and `gen` (each a dict with `points`, `morning` and `empty_at`; `gen` is None without
    a start), `end` (the right edge of the chart).
    """
    stop = generator_stop if generator_stop is not None else end
    longer = is_off(end - timedelta(minutes=1), off_intervals)
    far = end + timedelta(hours=max_hours) if longer else end
    off = off_intervals + [(end, far)] if longer else off_intervals
    lines = [simulate(battery, now, far, off)]
    if generator_start is not None:
        lines.append(simulate(battery, now, far, off, generator_start, stop))
    right = end + timedelta(hours=morning_hours) if longer else end
    found = []
    for line in lines:
        points = [point for point in line['points'] if point[0] <= end]
        morning = []
        if longer:
            usable = max(0.0, points[-1][1])
            for index in range(round(morning_hours * 4) + 1):
                hours = index / 4
                morning.append(
                    (
                        end + timedelta(hours=hours),
                        min(
                            battery['usable_max_kwh'],
                            usable + battery['generator_charge_kw'] * hours,
                        ),
                    )
                )
        found.append(
            {'points': points, 'morning': morning, 'empty_at': line['empty_at']}
        )
    return {
        'base': found[0],
        'gen': found[1] if len(found) > 1 else None,
        'end': right,
    }


def hours_until_empty(battery, now, max_hours):
    """Hours until the battery is empty without the city power and without the generator."""
    usable = battery['usable_now_kwh']
    if usable <= 0:
        return 0.0, now
    moment = now
    limit = now + timedelta(hours=max_hours)
    while moment < limit:
        step_end = min(limit, moment + battery['step'])
        cut = _cuts(moment, step_end, _window_edges(battery, moment))[0]
        hours = (cut - moment).total_seconds() / 3600
        drain = load_kw(battery, moment) * hours
        if drain >= usable:
            empty_at = moment + timedelta(hours=hours * usable / drain)
            return (empty_at - now).total_seconds() / 3600, empty_at
        usable = usable - drain
        moment = cut
    return float(max_hours), None


def _clock_steps(now, end, step):
    """`now`, then each moment of the clock grid of `step` before `end` (for 15 minutes: :00, :15, :30, :45).

    A start time on the clock grid is easy to read: 22:15, not 22:13.
    """
    found = [now]
    minutes = int(step.total_seconds() // 60)
    base = now.replace(second=0, microsecond=0)
    moment = base + timedelta(minutes=minutes - minutes_of_day(base) % minutes)
    while moment < end:
        found.append(moment)
        moment = moment + step
    return found


def _start_candidates(battery, now, end, off_intervals):
    """Each moment of the clock grid where the generator can start: in its window and without the city power."""
    found = []
    for moment in _clock_steps(now, end, battery['step']):
        if generator_allowed(battery, moment) and is_off(moment, off_intervals):
            found.append(moment)
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
    stops = _clock_steps(start, end, battery['step'])[1:] + [end]
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
        'stop_reason': '',
    }

    if generator_running:
        result['state'] = ADVICE_RUNNING
        if not is_off(now, off_intervals) or deficit <= 0:
            result['stop_at'] = now
            result['stop_reason'] = (
                'grid' if not is_off(now, off_intervals) else 'enough'
            )
            return result
        if not generator_allowed_now:
            result['enough'] = False
            result['stop_at'] = now
            result['stop_reason'] = 'window'
            return result
        stop = earliest_stop(battery, now, end, off_intervals, now)
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


def notice_stage(now, latest_start, stage_hours):
    """How many warnings before the latest start are due now: the count of `stage_hours` (for example [4, 2])
    with now >= latest start - hours. 0 without a latest start.

    The script sends "the generator will be necessary" once for each new stage, so people get it 4 hours and
    2 hours before the latest start (an early start lets them skip the morning start), and at once when the
    advice comes later than a stage.
    """
    if latest_start is None:
        return 0
    count = 0
    for hours in stage_hours:
        if now >= latest_start - timedelta(hours=hours):
            count += 1
    return count


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
        if advice.get('stop_reason') == 'grid':
            return 'Світло з міста є. Генератор можна вимкнути.'
        if advice.get('stop_reason') == 'window':
            return 'Генератор працює поза дозволеними годинами. Його треба вимкнути.'
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


# ==== TEXTS OF THE CHART AND OF ITS TELEGRAM CAPTION ====
# `data` is the input of `oktant_chart.draw` (see that module), built by the script.
# The chart and the caption show the same title and the same lines.


def _empty_after_forecast(data):
    """True when the battery goes empty without the generator, but only after the forecast end (the next window start)."""
    return data['empty_at'] is not None and data['empty_at'] > data['forecast_end']


def chart_headline(data):
    """The title (what to do, in plain words) and the badge before it: (title, badge, level).

    `level` is 'act' when people must do something, 'ok' when nothing is to do.
    """
    state = data['state']
    if state == ADVICE_START_NOW:
        return 'Увімкніть генератор зараз', 'Терміново', 'act'
    if state == ADVICE_NEEDED_LATER:
        return (
            f"Увімкніть генератор до {hhmm(data['latest_start'])}",
            'Потрібна дія',
            'act',
        )
    if state == ADVICE_RUNNING:
        if data.get('stop_reason') == 'window':
            closes = next_time_of_day(data['now'], data['window_end_minutes'])
            opens = next_time_of_day(data['now'], data['window_start_minutes'])
            return (
                f'Генератор треба вимкнути: з {hhmm(closes)} до {hhmm(opens)} він не працює',
                'Генератор працює',
                'act',
            )
        if data['stop_at'] is not None and data['stop_at'] <= data['now']:
            return 'Генератор можна вимкнути', 'Генератор працює', 'ok'
        return (
            f"Генератор працює. Можна вимкнути о {hhmm(data['stop_at'])}",
            'Генератор працює',
            'ok',
        )
    if state == ADVICE_OUTSIDE_HOURS:
        return 'Батарея може сісти вночі, а генератор вмикати не можна', 'Увага', 'act'
    if _empty_after_forecast(data):
        return 'Вночі генератор не потрібен', 'Вранці потрібна дія', 'act'
    if data['empty_at'] is not None:
        return 'Батарея може сісти вночі', 'Увага', 'act'
    return 'Генератор не потрібен', 'Все гаразд', 'ok'


def _power_back(data):
    """When the city power comes back, or None: the end of the outage that covers now, before the forecast end."""
    for start, stop in data['off_intervals']:
        if start <= data['now'] < stop < data['forecast_end']:
            return stop
    return None


def _power_off_now(data):
    for start, stop in data['off_intervals']:
        if start <= data['now'] < stop:
            return True
    return False


def summary_lines(data):
    """The lines under the title, each one on its own line: the battery without the generator
    and what the advised generator run gives."""
    forecast_end = data['forecast_end']
    lines = []
    if _empty_after_forecast(data):
        lines.append(
            f"З {hhmm(forecast_end)} генератор можна вмикати. Без нього батарея сяде о {hhmm(data['empty_at'])}."
        )
    elif data['empty_at'] is not None:
        lines.append(f"Без генератора батарея сяде о {hhmm(data['empty_at'])}.")
    else:
        lowest = data['points_base'][0]
        for point in data['points_base']:
            if point[0] <= forecast_end and point[1] < lowest[1]:
                lowest = point
        text = (
            f'Найменший заряд {lowest[1]:.0f}% о {hhmm(lowest[0])}, заряду вистачить.'
        )
        back = _power_back(data)
        if back is not None:
            text = f'Світло дадуть о {hhmm(back)}. ' + text
        elif not _power_off_now(data):
            text = 'Світло з міста є. ' + text
        lines.append(text)
    minutes = round(data['generator_hours'] * 60)
    # a generator that can stop now needs no sentence about its run
    if data['points_gen'] and data['latest_start'] is not None and minutes > 0:
        empty_gen_at = data.get('empty_gen_at')
        if empty_gen_at is not None and empty_gen_at <= forecast_end:
            lines.append(
                f'Генератору треба працювати {minutes} хв, але навіть з ним батарея сяде о {hhmm(empty_gen_at)}.'
            )
        else:
            lines.append(
                f'Генератору достатньо пропрацювати {minutes} хв, щоб батарея протрималася до {hhmm(forecast_end)}.'
            )
    return lines


def _value_at(points, moment):
    """The charge of a line at `moment`, straight between its points, or None outside the line."""
    previous = None
    for point in points:
        if point[0] == moment:
            return point[1]
        if point[0] > moment:
            if previous is None:
                return None
            share = (moment - previous[0]).total_seconds() / (
                point[0] - previous[0]
            ).total_seconds()
            return previous[1] + (point[1] - previous[1]) * share
        previous = point
    return None


CAPTION_MARKS = {
    ADVICE_NEEDED_LATER: '⚠️',
    ADVICE_START_NOW: '🔴',
    ADVICE_NOT_NEEDED: '🟢',
    ADVICE_RUNNING: '🟢',
    ADVICE_OUTSIDE_HOURS: '🌙',
}


def _planned(data):
    """True when the chart shows an advised run of the generator that has not started yet."""
    return (
        data['state'] != ADVICE_RUNNING
        and bool(data['points_gen'])
        and data['latest_start'] is not None
        and round(data['generator_hours'] * 60) > 0
    )


def caption_headline(data):
    """The line of the caption that tells what to do, with the emoji of the advice.

    For a run that has not started yet it also tells when the generator stops, for example
    "⚠️ Увімкніть генератор до 20:45, щоб він вимкнувся до 22:00".
    """
    mark = CAPTION_MARKS.get(data['state'], 'ℹ️')
    if data.get('stop_reason') == 'window':
        mark = '🌙'
    if _planned(data) and data['stop_at'] is not None:
        if data['state'] == ADVICE_START_NOW:
            action = 'Увімкніть генератор зараз'
        else:
            action = f"Увімкніть генератор до {hhmm(data['latest_start'])}"
        return f"{mark} {action}, щоб він вимкнувся до {hhmm(data['stop_at'])}"
    return f"{mark} {data['title']}"


def caption_lines(data, headlines=None):
    """The Telegram caption: the time and the charge, the city power, the lines of the event (`headlines`;
    without them `caption_headline`), then the key facts of the chart in plain words, one fact a line,
    each with an emoji. The order and the words are the user's sample."""
    now = data['now']
    forecast_end = data['forecast_end']
    zero = data['zero_percent']
    lines = [f"🕒 {hhmm(now)}, інвертор 🔋{data['points_base'][0][1]:.0f}%."]

    back = _power_back(data)
    if back is not None:
        lines.append(f'⚡ Світла з міста немає. За прогнозом дадуть о {hhmm(back)}.')
    elif _power_off_now(data):
        lines.append(
            f'⚡ Світла з міста немає. До {hhmm(forecast_end)} його не чекаємо.'
        )
    else:
        text = '⚡ Світло з міста є.'
        for start, stop in data['off_intervals']:
            if now < start < forecast_end:
                text = text + f' Відключення за графіком {hhmm(start)}–{hhmm(stop)}.'
                break
        lines.append(text)
    lines.extend(headlines if headlines else [caption_headline(data)])

    stop_at = data['stop_at']
    latest_start = data['latest_start']
    planned = _planned(data)
    if planned:
        minutes = round(data['generator_hours'] * 60)
        start_text = (
            'зараз' if data['state'] == ADVICE_START_NOW else hhmm(latest_start)
        )
        text = (
            f'⏱️ Генератору треба пропрацювати хоча б {minutes} хв: '
            f'з {start_text} до {hhmm(stop_at)}.'
        )
        value = _value_at(data['points_gen'], stop_at) if stop_at is not None else None
        if value is not None:
            text = text + f' Тоді заряд буде {value:.0f}%.'
        lines.append(text)

    empty_at = data['empty_at']
    window_end = next_time_of_day(now, data['window_end_minutes'])
    value = None
    if window_end <= forecast_end:
        value = _value_at(data['points_base'], window_end)
    if empty_at is not None and empty_at <= forecast_end:
        if value is not None and value > zero:
            lines.append(
                f'🪫 Без генератора о {hhmm(window_end)} заряд буде {value:.0f}%, '
                f'а батарея сяде о {hhmm(empty_at)}.'
            )
        else:
            lines.append(f'🪫 Без генератора батарея сяде о {hhmm(empty_at)}.')
    elif empty_at is not None:
        lines.append(
            f'🔋 Без генератора батарея протримається ніч, але сяде о {hhmm(empty_at)}, '
            f'якщо вранці не ввімкнути генератор.'
        )
    else:
        lowest = data['points_base'][0]
        for point in data['points_base']:
            if point[0] <= forecast_end and point[1] < lowest[1]:
                lowest = point
        lines.append(
            f'🔋 Без генератора заряду вистачить: найменший {lowest[1]:.0f}% о {hhmm(lowest[0])}.'
        )

    # only the bad case gets a line: the run is not enough to last the night
    empty_gen_at = data.get('empty_gen_at')
    if planned and empty_gen_at is not None and empty_gen_at <= forecast_end:
        lines.append(f'❗ Навіть з генератором батарея сяде о {hhmm(empty_gen_at)}.')
    return lines


def dot_notes(data):
    """Lines under the chart: what each dot means, as (kind of the dot or '', text).

    The kinds: 'empty' (the line without the generator), 'empty_gen' (with the generator).
    A line goes empty after the forecast end only when nobody starts the generator in the morning, so such a
    moment has no dot and no note.
    """
    forecast_end = data['forecast_end']
    notes = []
    empty_at = data['empty_at']
    if empty_at is not None and empty_at <= forecast_end:
        notes.append(
            (
                'empty',
                f'Помаранчева точка: без генератора інвертор вимкнеться о {hhmm(empty_at)}.',
            )
        )
    empty_gen_at = data.get('empty_gen_at')
    if data['points_gen'] and empty_gen_at is not None and empty_gen_at <= forecast_end:
        notes.append(
            (
                'empty_gen',
                f'Зелена точка: з генератором інвертор вимкнеться о {hhmm(empty_gen_at)}.',
            )
        )
    if data.get('morning_base') or data.get('morning_gen'):
        notes.append(
            ('', f'О {hhmm(forecast_end)} генератор вмикається, і заряд знову росте.')
        )
    if not notes:
        notes.append(('', 'Лінія показує заряд батареї з часом.'))
    return notes
