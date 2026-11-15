# https://github.com/custom-components/pyscript
"""Chart of the battery forecast of the Oktant A Invertor, in plain Ukrainian for a person without chart skills.

This file is plain Python with Pillow. pyscript does not import it. The script
`pyscript/oktant_generator_advisor.py` loads it inside a `@pyscript_executor` function with importlib,
because drawing and file writes block the event loop. A local test can import it directly.

Input of `draw(data, path, font_paths)`: a dict with
- `now`, `end`: aware datetimes, the start and the end of the forecast.
- `points_base`: list of (datetime, percent): the charge without the generator.
- `points_gen`: list of (datetime, percent) or empty: the charge with the generator from the latest start.
- `zero_percent`: the charge where the inverter turns off.
- `window_start_minutes`, `window_end_minutes`: the generator window (minutes of the day).
- `off_intervals`: list of (start, end) without city power.
- `state`: the advice state (`not_needed`, `needed_later`, `start_now`, `running`, `outside_hours`).
- `latest_start`, `stop_at`, `empty_at`: datetimes or None.
- `generator_hours`: hours of the generator run.
- `demo`: True adds a "demo" mark.
`font_paths`: (regular, bold) candidates; the first file that exists is used.
"""

import os
from datetime import timedelta

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 780
LEFT = 90
RIGHT = 40
TOP = 210
BOTTOM = 150

BACKGROUND = (250, 250, 247)
TEXT = (33, 37, 41)
MUTED = (110, 116, 122)
GRID = (226, 228, 230)
NIGHT = (228, 233, 247)
RED_ZONE = (253, 226, 226)
RED = (205, 45, 45)
ORANGE = (230, 120, 20)
GREEN = (30, 150, 80)
POWER_ON = (255, 214, 92)
POWER_OFF = (150, 155, 160)
# an hour label closer than this to a key label (now, 23:00, 07:00) is not drawn
KEY_LABEL_GAP_PX = 70


def _font(paths, size):
    for path in paths:
        if path and os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def _hhmm(moment):
    return moment.strftime('%H:%M') if moment is not None else '—'


def _value_at(points, moment):
    value = points[0][1]
    for point_moment, percent in points:
        if point_moment > moment:
            break
        value = percent
    return value


def _in_window(moment, start, end):
    minute = moment.hour * 60 + moment.minute
    return start <= minute < end


def _wrap(d, text, font, width):
    lines = []
    current = ''
    for word in text.split(' '):
        candidate = word if not current else current + ' ' + word
        if d.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _next_time(now, minutes):
    candidate = now.replace(
        hour=minutes // 60, minute=minutes % 60, second=0, microsecond=0
    )
    if candidate <= now:
        candidate = candidate + timedelta(days=1)
    return candidate


def axis_ticks(now, end, window_end_minutes, plot_width):
    """Labels under the time axis: list of (moment, label, key).

    The key labels always show: now, the end of the generator window (23:00) and the end of the forecast (07:00).
    A label of an even hour shows only when it does not come too near a key label.
    """
    min_gap = (end - now).total_seconds() * KEY_LABEL_GAP_PX / plot_width
    keys = [(now, f'зараз {_hhmm(now)}', True)]
    window_end = _next_time(now, window_end_minutes)
    if window_end < end:
        keys.append((window_end, _hhmm(window_end), True))
    keys.append((end, _hhmm(end), True))
    ticks = list(keys)
    tick = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    while tick < end:
        near = False
        for moment, _, _ in keys:
            if abs((tick - moment).total_seconds()) < min_gap:
                near = True
        if tick.hour % 2 == 0 and not near:
            ticks.append((tick, f'{tick.hour:02d}:00', False))
        tick = tick + timedelta(hours=1)
    ticks.sort(key=lambda item: item[0])
    return ticks


def headline(data):
    """Big text at the top: what to do, in plain words."""
    state = data['state']
    if state == 'start_now':
        return 'Увімкніть генератор зараз', RED
    if state == 'needed_later':
        return (
            f"Генератор знадобиться: увімкніть до {_hhmm(data['latest_start'])}",
            ORANGE,
        )
    if state == 'running':
        return f"Генератор працює. Можна вимкнути о {_hhmm(data['stop_at'])}", GREEN
    if state == 'outside_hours':
        return 'Батарея може сісти вночі, а генератор зараз вмикати не можна', RED
    return 'Генератор не потрібен', GREEN


def subline(data):
    """Second line: what happens without the generator, and what the generator gives."""
    parts = []
    if data['empty_at'] is not None:
        parts.append(
            f"Без генератора світло в будинку зникне приблизно о {_hhmm(data['empty_at'])}."
        )
    else:
        parts.append(f"Батарея протримається до {_hhmm(data['end'])}.")
    if data['points_gen'] and data['latest_start'] is not None:
        minutes = round(data['generator_hours'] * 60)
        parts.append(
            f"Генератору досить попрацювати приблизно {minutes} хв, з {_hhmm(data['latest_start'])} до {_hhmm(data['stop_at'])}."
        )
    return ' '.join(parts)


def draw(data, path, font_paths):
    regular_paths, bold_paths = font_paths
    f_title = _font(bold_paths, 34)
    f_sub = _font(regular_paths, 22)
    f_label = _font(regular_paths, 18)
    f_label_bold = _font(bold_paths, 18)
    f_small = _font(regular_paths, 16)

    now = data['now']
    end = data['end']
    total = (end - now).total_seconds()
    zero = data['zero_percent']
    plot_w = WIDTH - LEFT - RIGHT
    plot_h = HEIGHT - TOP - BOTTOM
    image = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    d = ImageDraw.Draw(image)

    def x_of(moment):
        return LEFT + plot_w * max(
            0.0, min(1.0, (moment - now).total_seconds() / total)
        )

    def y_of(percent):
        return TOP + plot_h * (1 - max(0.0, min(100.0, percent)) / 100)

    # headline and explanation
    title, title_color = headline(data)
    if data.get('demo'):
        title = 'ДЕМО. ' + title
    d.text((LEFT, 24), title, fill=title_color, font=f_title)
    y = 72
    for line in _wrap(d, subline(data), f_sub, WIDTH - LEFT - RIGHT):
        d.text((LEFT, y), line, fill=TEXT, font=f_sub)
        y += 28

    # strip: city power yes or no
    strip_y = TOP - 42
    d.text((LEFT, strip_y - 26), 'Світло з міста:', fill=MUTED, font=f_small)
    moment = now
    step = timedelta(minutes=15)
    while moment < end:
        off = False
        for start, stop in data['off_intervals']:
            if start <= moment < stop:
                off = True
        nxt = min(end, moment + step)
        d.rectangle(
            [x_of(moment), strip_y, x_of(nxt), strip_y + 16],
            fill=POWER_OFF if off else POWER_ON,
        )
        moment = nxt
    d.rectangle(
        [LEFT + plot_w - 340, strip_y - 24, LEFT + plot_w - 326, strip_y - 10],
        fill=POWER_ON,
    )
    d.text((LEFT + plot_w - 320, strip_y - 27), 'є світло', fill=MUTED, font=f_small)
    d.rectangle(
        [LEFT + plot_w - 230, strip_y - 24, LEFT + plot_w - 216, strip_y - 10],
        fill=POWER_OFF,
    )
    d.text(
        (LEFT + plot_w - 210, strip_y - 27),
        'немає світла (прогноз)',
        fill=MUTED,
        font=f_small,
    )

    # night: the generator cannot run. The forecast ends at the start of the window, so the night ends there.
    spans = []
    if not _in_window(now, data['window_start_minutes'], data['window_end_minutes']):
        spans.append((now, end))
    else:
        night_start = _next_time(now, data['window_end_minutes'])
        if night_start < end:
            spans.append((night_start, end))
    for start, stop in spans:
        d.rectangle([x_of(start), TOP, x_of(stop), TOP + plot_h], fill=NIGHT)
        label = 'Ніч: генератор не вмикаємо'
        width = d.textlength(label, font=f_label)
        if x_of(stop) - x_of(start) > width + 20:
            d.text(
                ((x_of(start) + x_of(stop) - width) / 2, TOP + 10),
                label,
                fill=(80, 95, 150),
                font=f_label,
            )

    # red zone: the house has no power
    d.rectangle([LEFT, y_of(zero), LEFT + plot_w, TOP + plot_h], fill=RED_ZONE)
    d.line([LEFT, y_of(zero), LEFT + plot_w, y_of(zero)], fill=RED, width=2)
    d.text(
        (LEFT + 10, y_of(zero) + 6),
        f'Нижче {zero:.0f}% інвертор вимикається: світла в будинку немає',
        fill=RED,
        font=f_label,
    )

    # grid and axes
    for percent in range(0, 101, 25):
        y = y_of(percent)
        d.line([LEFT, y, LEFT + plot_w, y], fill=GRID)
        d.text((LEFT - 52, y - 10), f'{percent}%', fill=MUTED, font=f_label)
    d.text((14, TOP - 30), 'Заряд', fill=MUTED, font=f_small)
    # a label that would cover the label before it goes to the second row
    row_right = [LEFT - 100.0, LEFT - 100.0]
    for moment, label, key in axis_ticks(now, end, data['window_end_minutes'], plot_w):
        x = x_of(moment)
        font = f_label_bold if key else f_label
        width = d.textlength(label, font=font)
        lx = max(LEFT - 20, min(x - width / 2, WIDTH - RIGHT - width))
        row = 0 if lx > row_right[0] + 8 else 1
        row_right[row] = lx + width
        d.line(
            [x, TOP + plot_h, x, TOP + plot_h + (10 + 24 * row if key else 6)],
            fill=TEXT if key else MUTED,
            width=2 if key else 1,
        )
        d.text(
            (lx, TOP + plot_h + 12 + 24 * row),
            label,
            fill=TEXT if key else MUTED,
            font=font,
        )

    # latest start
    if data['latest_start'] is not None and data['points_gen']:
        x = x_of(data['latest_start'])
        for y in range(TOP, int(y_of(zero)) - 7, 14):
            d.line([x, y, x, y + 7], fill=GREEN, width=2)
        label = f"Крайній час увімкнути генератор: {_hhmm(data['latest_start'])}"
        width = d.textlength(label, font=f_label_bold)
        lx = x - width - 10 if x + width + 10 > LEFT + plot_w else x + 10
        d.text((lx, TOP + 40), label, fill=GREEN, font=f_label_bold)

    # lines
    if data['points_gen']:
        d.line([(x_of(m), y_of(p)) for m, p in data['points_gen']], fill=GREEN, width=5)
    base = [(x_of(m), y_of(p)) for m, p in data['points_base']]
    d.line(base, fill=ORANGE, width=5)

    # labels on the lines: orange below its line, green above its line, both after the latest start
    label_at = now + (end - now) * 0.55
    base_y = _value_at(data['points_base'], label_at)
    d.text(
        (x_of(label_at) - 70, y_of(base_y) + 24),
        'Без генератора',
        fill=ORANGE,
        font=f_label_bold,
    )
    if data['points_gen']:
        gen_y = _value_at(data['points_gen'], label_at)
        d.text(
            (x_of(label_at) - 70, y_of(gen_y) - 36),
            'З генератором',
            fill=GREEN,
            font=f_label_bold,
        )

    # now
    first = data['points_base'][0]
    x0, y0 = x_of(now), y_of(first[1])
    d.ellipse([x0 - 7, y0 - 7, x0 + 7, y0 + 7], fill=TEXT)
    d.text((x0 + 12, y0 - 34), f'Зараз {first[1]:.0f}%', fill=TEXT, font=f_label_bold)

    # moment when the battery goes empty
    if data['empty_at'] is not None and data['empty_at'] <= end:
        xe, ye = x_of(data['empty_at']), y_of(zero)
        d.ellipse([xe - 8, ye - 8, xe + 8, ye + 8], fill=RED)
        label = f"Світло зникне ≈ {_hhmm(data['empty_at'])}"
        width = d.textlength(label, font=f_label_bold)
        d.text(
            (max(LEFT, xe - width - 16), ye + 12), label, fill=RED, font=f_label_bold
        )

    # how to read
    d.text(
        (LEFT, HEIGHT - 70),
        'Як читати: лінія показує, скільки заряду лишиться в батареї з часом. Коли лінія опускається',
        fill=MUTED,
        font=f_small,
    )
    d.text(
        (LEFT, HEIGHT - 48),
        'в червону зону, будинок залишиться без світла. Зелена лінія показує, як генератор додає заряд.',
        fill=MUTED,
        font=f_small,
    )
    d.text(
        (WIDTH - RIGHT - 170, HEIGHT - 48),
        f"Прогноз на {_hhmm(now)}",
        fill=MUTED,
        font=f_small,
    )

    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    image.save(path)
    return path
