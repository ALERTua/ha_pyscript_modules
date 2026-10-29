# https://github.com/custom-components/pyscript
from imports_base import *


def _outage_time(dt_, day):
    # an outage up to midnight ends at 00:00 of the next day
    if dt_.date() > day and dt_.hour == 0 and dt_.minute == 0:
        return '24:00'
    return dt_.strftime('%H:%M')


def outage_schedule_message(events, now):
    """Return the text for the neighbours, or None when no outages are planned."""
    if not events:
        return None

    today = now.date()
    tomorrow = today + timedelta(days=1)
    msg = '💡🗓️ Оновлений графік відключень:'
    for e in sorted(events, key=lambda e: e.start):
        day = e.start.date()
        if e.description == 'Emergency':
            # emergency outages are a mode of today only, with no schedule
            msg += '\n - ⚠️ екстрені відключення'
            continue

        line = f"{_outage_time(e.start, day)}–{_outage_time(e.end, day)}"
        if day == tomorrow:
            line += ' (завтра)'
        elif day != today:
            line += f" ({day.strftime('%d.%m')})"

        msg += f"\n - {line}"

    return msg
