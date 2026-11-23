# https://github.com/custom-components/pyscript
"""Chart of the battery forecast of the Oktant A Invertor, in plain Ukrainian for a person without chart skills.

This file is plain Python with Pillow. pyscript does not import it. The script
`pyscript/oktant_generator_advisor.py` loads it inside a `@pyscript_executor` function with importlib,
because drawing and file writes block the event loop. A local test can import it directly.

Input of `draw(data, path, font_paths)`: a dict with
- `now`, `end`: aware datetimes, the left and the right edge of the chart.
- `forecast_end`: the end of the forecast (the next start of the generator window, for example 08:00). Without the city
  power at that moment, `end` is later, so that the chart shows the morning run of the generator.
  Without the key, the forecast ends at `end`.
- `points_base`: list of (datetime, percent): the charge without the generator.
- `points_gen`: list of (datetime, percent) or empty: the charge with the generator from the latest start.
- `morning_base`, `morning_gen` (optional): lists of (datetime, percent) from `forecast_end`: the charge of each
  line when people start the generator as the window opens. A line that is empty before then grows from the zero
  point, so it has a gap while the inverter is off.
- `zero_percent`: the charge where the inverter turns off.
- `window_start_minutes`, `window_end_minutes`: the generator window (minutes of the day).
- `off_intervals`: list of (start, end) without city power.
- `state`: the advice state (`not_needed`, `needed_later`, `start_now`, `running`, `outside_hours`).
- `latest_start`, `stop_at`, `empty_at`: datetimes or None.
- `empty_gen_at` (optional): datetime or None, the moment when the line with the generator goes empty.
- `generator_hours`: hours of the generator run.
- `title`, `badge`, `badge_level` ('act' or 'ok'), `lines` (the lines under the title) and `notes` (list of
  (kind of the dot or '', text) under the chart): the texts, from `oktant_forecast.chart_headline`,
  `summary_lines` and `dot_notes`. The Telegram caption uses the same texts.
- `demo`: True adds a "demo" tag.
`font_paths`: (regular, bold) candidates; the first file that exists is used.

Colors: orange and green mean only the lines (without and with the generator) and their marks. The badge
before the title is red when people must act, green when nothing is to do. The title itself is dark text.
"""

import math
import os
from datetime import timedelta

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 906
LEFT = 90
RIGHT = 40
TOP = 258
# the axis has up to four rows: the hours, the event times and "зараз", "Крайній старт", a word that gives way;
# the notes follow
BOTTOM = 228
# at most this many lines of text under the title
SUMMARY_MAX_LINES = 4

BACKGROUND = (250, 250, 247)
TEXT = (33, 37, 41)
MUTED = (95, 101, 107)
GRID = (226, 228, 230)
NIGHT = (228, 233, 247)
# the dashed edges of the night: the blue of the night, darker, so that the dashes show on the light background
NIGHT_EDGE = (160, 174, 222)
NIGHT_TEXT = (80, 95, 150)
RED_ZONE = (253, 226, 226)
RED = (205, 45, 45)
ORANGE = (230, 120, 20)
GREEN = (30, 150, 80)
WHITE = (255, 255, 255)
POWER_ON = (255, 214, 92)
POWER_OFF = (150, 155, 160)
# an hour label closer than this to a key label (now, 23:00, 07:00) is not drawn
KEY_LABEL_GAP_PX = 80
# the gap between a line and its label ("Без генератора", "З генератором")
LINE_LABEL_GAP_PX = 6
# the smallest gap between two labels on the charge scale, pixels
Y_MARK_GAP_PX = 20
# the width of the two lines, pixels
LINE_WIDTH = 3
# the lines, the dots and the labels on the lines are drawn this many times larger and then made smaller,
# so that their edges are smooth
LINE_SCALE = 4
# where a label of a line can sit, as a share of the chart width, in the order of the tries
LINE_LABEL_SHARES = [
    0.55,
    0.5,
    0.6,
    0.45,
    0.65,
    0.4,
    0.7,
    0.35,
    0.75,
    0.3,
    0.8,
    0.25,
    0.85,
    0.2,
    0.9,
    0.15,
    0.1,
]
# the event times (latest start, inverter off) go to the second row under the axis
EVENT_KINDS = ('start', 'empty', 'empty_gen')


def _font(paths, size):
    for path in paths:
        if path and os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def _hhmm(moment):
    return moment.strftime('%H:%M') if moment is not None else '—'


def _until_level(points, level):
    """The points of a line up to the moment when it reaches `level`, with the last point exactly at `level`.

    The inverter turns off at the zero point, so the battery does not go lower: the line ends there.
    """
    found = []
    for point in points:
        if point[1] > level:
            found.append(point)
            continue
        if found:
            previous = found[-1]
            share = (previous[1] - level) / (previous[1] - point[1])
            found.append((previous[0] + (point[0] - previous[0]) * share, float(level)))
        else:
            found.append((point[0], float(level)))
        break
    return found


def _overlaps(box, boxes):
    """True when the box (left, top, right, bottom) overlaps one of `boxes`."""
    for other in boxes:
        if (
            box[0] < other[2]
            and other[0] < box[2]
            and box[1] < other[3]
            and other[1] < box[3]
        ):
            return True
    return False


def _interpolate(points, moment):
    """The value of the line at `moment`, on the straight part between the two points around it."""
    previous = points[0]
    for point in points:
        if point[0] >= moment:
            span = (point[0] - previous[0]).total_seconds()
            if span <= 0:
                return point[1]
            share = (moment - previous[0]).total_seconds() / span
            return previous[1] + (point[1] - previous[1]) * share
        previous = point
    return previous[1]


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


def axis_ticks(
    now, end, window_end_minutes, plot_width, forecast_end=None, start=None, marks=None
):
    """Labels under the time axis: list of (moment, label, kind).

    `kind` is 'now', 'key', 'start', a kind of `marks` or '' (an hour label). The labels of now, of the end of
    the generator window (23:00) and of the end of the forecast (07:00) always show. The latest start of the
    generator (`start`) always shows too, under the green dashed line, and so does each (moment, kind) of `marks`:
    the moments when the inverter turns off ('empty' without the generator, 'empty_gen' with it).
    The event times (`EVENT_KINDS`) go to the second row, so an hour label gives way only to now, 23:00 and 07:00.
    """
    if forecast_end is None:
        forecast_end = end
    min_gap = (end - now).total_seconds() * KEY_LABEL_GAP_PX / plot_width
    # the word "зараз" stands under this time (`draw`)
    keys = [(now, _hhmm(now), 'now')]
    window_end = _next_time(now, window_end_minutes)
    if window_end < forecast_end:
        keys.append((window_end, _hhmm(window_end), 'key'))
    keys.append((forecast_end, _hhmm(forecast_end), 'key'))
    events = []
    if start is not None and now < start < end:
        events.append((start, _hhmm(start), 'start'))
    for moment, kind in marks or []:
        if moment is not None and now < moment <= end:
            events.append((moment, _hhmm(moment), kind))
    ticks = keys + events
    tick = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    while tick < end:
        near = False
        for moment, _, _ in keys:
            if abs((tick - moment).total_seconds()) < min_gap:
                near = True
        if tick.hour % 2 == 0 and not near:
            ticks.append((tick, f'{tick.hour:02d}:00', ''))
        tick = tick + timedelta(hours=1)
    ticks.sort(key=lambda item: item[0])
    return ticks


def _hits_line(center, direction, size, lines, moment_of, y_of, value_at):
    """True when one of `lines` runs through a turned rectangle (3 pixels of margin).

    `center` and `size` (width along the line, height) are in pixels; `direction` is the unit vector along the text.
    """
    (cx, cy), (ux, uy), (width, height) = center, direction, size
    steps = max(2, math.ceil(width / 8))
    for points in lines:
        for i in range(steps + 1):
            along = width * (i / steps - 0.5)
            for across in (-height / 2, 0.0, height / 2):
                px = cx + ux * along - uy * across
                py = cy + uy * along + ux * across
                moment = moment_of(px)
                if not points[0][0] <= moment <= points[-1][0]:
                    continue
                if abs(py - y_of(value_at(points, moment))) <= LINE_WIDTH / 2 + 3:
                    return True
    return False


def _badge(d, x, y, text, color, font):
    """A rounded box with white text. Returns its right edge."""
    width = d.textlength(text, font=font)
    box = d.textbbox((0, 0), text, font=font)
    height = box[3] - box[1]
    d.rounded_rectangle(
        [x, y, x + width + 24, y + height + 16], radius=(height + 16) // 2, fill=color
    )
    d.text((x + 12, y + 8 - box[1]), text, fill=WHITE, font=font)
    return x + width + 24


def draw(data, path, font_paths):
    regular_paths, bold_paths = font_paths
    f_sub = _font(regular_paths, 21)
    f_label = _font(regular_paths, 18)
    f_label_bold = _font(bold_paths, 18)
    f_small = _font(regular_paths, 16)
    f_small_bold = _font(bold_paths, 16)
    f_line_label = _font(bold_paths, 18 * LINE_SCALE)

    now = data['now']
    end = data['end']
    forecast_end = data.get('forecast_end', end)
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

    def moment_of(x):
        return now + timedelta(seconds=total * (x - LEFT) / plot_w)

    # each line ends at the zero point: the inverter turns off there, and the battery goes no lower
    points_base = _until_level(data['points_base'], zero)
    points_gen = _until_level(data['points_gen'], zero) if data['points_gen'] else []

    # the demo tag in the top right corner, the badge and the title; a long title gets a smaller font
    title_right = WIDTH - RIGHT
    if data.get('demo'):
        width = d.textlength('ДЕМО', font=f_small_bold)
        _badge(d, WIDTH - RIGHT - width - 24, 8, 'ДЕМО', MUTED, f_small_bold)
        title_right = WIDTH - RIGHT - width - 34
    title = data['title']
    badge_color = RED if data['badge_level'] == 'act' else GREEN
    x = _badge(d, LEFT, 30, data['badge'], badge_color, f_label_bold) + 14
    size = 34
    f_title = _font(bold_paths, size)
    while size > 24 and x + d.textlength(title, font=f_title) > title_right:
        size -= 2
        f_title = _font(bold_paths, size)
    box = d.textbbox((0, 0), title, font=f_title)
    d.text((x, 47 - (box[1] + box[3]) / 2), title, fill=TEXT, font=f_title)
    y = 80
    shown = []
    for part in data['lines']:
        shown.extend(_wrap(d, part, f_sub, WIDTH - LEFT - RIGHT))
    for line in shown[:SUMMARY_MAX_LINES]:
        d.text((LEFT, y), line, fill=TEXT, font=f_sub)
        y += 27

    # strip: city power yes or no; the legend names only the colors that the strip shows
    strip_y = TOP - 42
    d.text((LEFT, strip_y - 26), 'Світло з міста:', fill=MUTED, font=f_small)
    d.rectangle([x_of(now), strip_y, x_of(end), strip_y + 16], fill=POWER_ON)
    off_width = 0.0
    for start, stop in data['off_intervals']:
        start = max(now, start)
        stop = min(end, stop)
        if start < stop:
            d.rectangle(
                [x_of(start), strip_y, x_of(stop), strip_y + 16], fill=POWER_OFF
            )
            off_width += x_of(stop) - x_of(start)
    legend = []
    if off_width < plot_w - 1:
        legend.append((POWER_ON, 'є світло'))
    if off_width > 0:
        legend.append((POWER_OFF, 'немає світла'))
    lx = LEFT + plot_w
    for color, label in reversed(legend):
        lx -= d.textlength(label, font=f_small)
        d.text((lx, strip_y - 27), label, fill=MUTED, font=f_small)
        lx -= 20
        d.rectangle([lx, strip_y - 24, lx + 14, strip_y - 10], fill=color)
        lx -= 24

    # night: the generator cannot run. The forecast ends at the start of the window, so the night ends there.
    spans = []
    if not _in_window(now, data['window_start_minutes'], data['window_end_minutes']):
        spans.append((now, forecast_end))
    else:
        night_start = _next_time(now, data['window_end_minutes'])
        if night_start < forecast_end:
            spans.append((night_start, forecast_end))
    # boxes of the texts and the dashed lines inside the plot, so that the labels of the lines do not cover them
    taken = []
    for start, stop in spans:
        d.rectangle([x_of(start), TOP, x_of(stop), TOP + plot_h], fill=NIGHT)
        # the edges of the night as dashed lines, except an edge that is the edge of the chart
        for edge in (start, stop):
            if now < edge < end:
                x = x_of(edge)
                for y in range(TOP, TOP + plot_h, 14):
                    d.line([x, y, x, y + 7], fill=NIGHT_EDGE, width=2)
                taken.append((x - 3, TOP, x + 3, TOP + plot_h))
        label = 'Ніч: генератор не вмикаємо'
        width = d.textlength(label, font=f_label)
        if x_of(stop) - x_of(start) > width + 20:
            position = ((x_of(start) + x_of(stop) - width) / 2, TOP + 10)
            d.text(position, label, fill=NIGHT_TEXT, font=f_label)
            taken.append(d.textbbox(position, label, font=f_label))

    # red zone: the house has no power
    d.rectangle([LEFT, y_of(zero), LEFT + plot_w, TOP + plot_h], fill=RED_ZONE)
    d.line([LEFT, y_of(zero), LEFT + plot_w, y_of(zero)], fill=RED, width=2)
    position = (LEFT + 10, y_of(zero) + 6)
    label = f'Нижче {zero:.0f}% інвертор вимикається'
    d.text(position, label, fill=RED, font=f_label)
    taken.append(d.textbbox(position, label, font=f_label))

    # marks on the charge scale: the charge now, the zero point (13 %), the charge without the generator at the end
    # of the generator window (23:00) and the charge with the generator when it stops (23:00).
    # Each mark of a later moment has a dashed line to a dot on its line.
    y_marks = [(now, data['points_base'][0][1], TEXT), (None, zero, RED)]
    window_end = _next_time(now, data['window_end_minutes'])
    if now < window_end <= forecast_end and window_end <= points_base[-1][0]:
        value = _interpolate(points_base, window_end)
        if value > zero:
            y_marks.append((window_end, value, ORANGE))
    if points_gen and data['stop_at'] is not None:
        value = _interpolate(points_gen, data['stop_at'])
        y_marks.append((data['stop_at'], value, GREEN))
    # the charge with the generator when the night ends (the owner's wish): how the battery leaves the night.
    # A dot with the number next to it, no mark on the scale.
    night_exit = None
    if (
        points_gen
        and now < forecast_end <= points_gen[-1][0]
        and forecast_end != data['stop_at']
    ):
        value = _interpolate(points_gen, forecast_end)
        if value > zero + 0.5:
            night_exit = (x_of(forecast_end), y_of(value), f'{value:.0f}%')

    # grid and axes; a grid label near a mark gives way to the mark
    for percent in range(0, 101, 25):
        y = y_of(percent)
        d.line([LEFT, y, LEFT + plot_w, y], fill=GRID)
        near = False
        for _, value, _ in y_marks:
            if abs(y - y_of(value)) < Y_MARK_GAP_PX:
                near = True
        if not near:
            label = f'{percent}%'
            width = d.textlength(label, font=f_label)
            d.text((LEFT - 12 - width, y - 11), label, fill=MUTED, font=f_label)
    # the labels of the marks keep Y_MARK_GAP_PX from each other: from the top down, a label moves down
    label_y = TOP - 100.0
    for moment, value, color in sorted(y_marks, key=lambda mark: -mark[1]):
        y = y_of(value)
        label_y = max(y, label_y + Y_MARK_GAP_PX)
        label = f'{value:.0f}%'
        width = d.textlength(label, font=f_label_bold)
        d.text((LEFT - 12 - width, label_y - 11), label, fill=color, font=f_label_bold)
        d.line([LEFT - 8, y, LEFT, y], fill=color, width=2)
        if moment is not None:
            for x in range(LEFT, int(x_of(moment)) - 6, 10):
                d.line([x, y, x + 5, y], fill=color, width=1)

    # time axis: now, the window end, the forecast end and the hours in the first row, the event times in their
    # colors in the second row. A line goes empty after the forecast end only without the morning generator, so
    # such a moment gets no dot and no time.
    start_label = data['latest_start'] if points_gen else None
    empty_at = data['empty_at']
    if empty_at is not None and empty_at > forecast_end:
        empty_at = None
    empty_gen_at = data.get('empty_gen_at') if points_gen else None
    if empty_gen_at is not None and empty_gen_at > forecast_end:
        empty_gen_at = None
    marks = [(empty_at, 'empty'), (empty_gen_at, 'empty_gen')]
    colors = {'start': GREEN, 'empty': ORANGE, 'empty_gen': GREEN}
    row_right = [LEFT - 100.0, LEFT - 100.0]
    # the boxes of the axis texts as (row, left, right), and the words under a time: (center, words, color, row)
    row_boxes = []
    under = []
    for moment, label, kind in axis_ticks(
        now, end, data['window_end_minutes'], plot_w, forecast_end, start_label, marks
    ):
        x = x_of(moment)
        row = 1 if kind in EVENT_KINDS else 0
        font = f_label_bold if kind in ('now', *EVENT_KINDS) else f_label
        color = colors.get(kind, TEXT if kind else MUTED)
        width = d.textlength(label, font=font)
        lx = max(LEFT - 20, min(x - width / 2, WIDTH - RIGHT - width))
        if row == 1:
            lx = max(lx, row_right[1] + 8)
        elif lx < row_right[0] + 8 and not kind:
            continue
        row_right[row] = lx + width
        d.line(
            [x, TOP + plot_h, x, TOP + plot_h + (34 if row else 8)],
            fill=color,
            width=2 if kind else 1,
        )
        d.text((lx, TOP + plot_h + 12 + 24 * row), label, fill=color, font=font)
        row_boxes.append((row, lx, lx + width))
        # words under a time (the owner's choice): "зараз" under the time now, "Крайній старт" under the latest start
        if kind == 'now':
            under.append((lx + width / 2, 'зараз', TEXT, 1))
        elif kind == 'start':
            under.append((lx + width / 2, 'Крайній старт', GREEN, 2))

    # each word goes to the first free row from its own row down, so that two words never overlap
    for center, words, color, row in under:
        words_width = d.textlength(words, font=f_label_bold)
        wx = max(LEFT - 20, min(center - words_width / 2, WIDTH - RIGHT - words_width))
        free = False
        while not free:
            free = True
            for box_row, left, right in row_boxes:
                if box_row == row and wx < right + 8 and left < wx + words_width + 8:
                    free = False
            if not free:
                row += 1
        row_boxes.append((row, wx, wx + words_width))
        d.text((wx, TOP + plot_h + 12 + 24 * row), words, fill=color, font=f_label_bold)

    # latest start: the dashed line. Its box goes to `taken`, so that the labels of the lines do not cross it.
    if data['latest_start'] is not None and points_gen:
        x = x_of(data['latest_start'])
        for y in range(TOP, int(y_of(zero)) - 7, 14):
            d.line([x, y, x, y + 7], fill=GREEN, width=2)
        taken.append((x - 3, TOP, x + 3, y_of(zero)))

    # moments when the inverter turns off: a dashed line from the dot down to its time under the axis.
    # The text under the chart tells in words what each dot means.
    dots = [(empty_at, ORANGE)]
    if empty_gen_at is not None:
        dots.append((empty_gen_at, GREEN))
    empty_dots = []
    for moment, color in dots:
        if moment is None or moment > end:
            continue
        xe, ye = x_of(moment), y_of(zero)
        for y in range(int(ye) + 10, TOP + plot_h, 10):
            d.line([xe, y, xe, y + 5], fill=color, width=2)
        empty_dots.append((xe, ye, 7, color))

    # the lines and the dots, drawn LINE_SCALE times larger and then made smaller: smooth edges.
    # A white ring around each dot keeps it apart from the red line under it.
    x0, y0 = x_of(now), y_of(data['points_base'][0][1])
    layer = Image.new('RGBA', (WIDTH * LINE_SCALE, HEIGHT * LINE_SCALE), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # the morning parts: people start the generator when the window opens, and the charge grows again
    lines = [(points_base, ORANGE), (data.get('morning_base') or [], ORANGE)]
    if points_gen:
        lines.insert(0, (data.get('morning_gen') or [], GREEN))
        lines.insert(0, (points_gen, GREEN))
    for points, color in lines:
        xy = [(x_of(m) * LINE_SCALE, y_of(p) * LINE_SCALE) for m, p in points]
        if len(xy) > 1:
            ld.line(xy, fill=color, width=LINE_WIDTH * LINE_SCALE, joint='curve')
    round_dots = [(x0, y0, 6, TEXT)] + empty_dots
    for moment, value, color in y_marks:
        if moment is not None and moment > now:
            round_dots.append((x_of(moment), y_of(value), 6, color))
    if night_exit is not None:
        round_dots.append((night_exit[0], night_exit[1], 6, GREEN))
    for x, y, r, color in round_dots:
        ld.ellipse(
            [
                (x - r) * LINE_SCALE,
                (y - r) * LINE_SCALE,
                (x + r) * LINE_SCALE,
                (y + r) * LINE_SCALE,
            ],
            fill=color,
            outline=WHITE,
            width=2 * LINE_SCALE,
        )
    layer = layer.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    image.paste(layer, (0, 0), layer)

    # the number of the charge at the end of the night: right of its dot, above the line that grows from there
    if night_exit is not None:
        box = d.textbbox((0, 0), night_exit[2], font=f_label_bold)
        tx = min(night_exit[0] + 10, LEFT + plot_w - (box[2] - box[0]))
        ty = night_exit[1] - 12 - (box[3] - box[1])
        # the line grows to the right: the number stays above it over its whole width
        morning = data.get('morning_gen') or []
        right = moment_of(tx + box[2] - box[0])
        if morning and morning[0][0] <= right <= morning[-1][0]:
            ty = min(ty, y_of(_interpolate(morning, right)) - 8 - (box[3] - box[1]))
        d.text((tx, ty), night_exit[2], fill=GREEN, font=f_label_bold)
        taken.append(d.textbbox((tx, ty), night_exit[2], font=f_label_bold))

    # labels on the lines: orange below its line, green above it, turned along the line, near the middle of the chart.
    # A label sits only where the line is straight under it; when it covers another text or leaves the plot,
    # it moves along its line to the next place.
    # each line gets the sides where it may sit, the first is the one it likes, and the other lines it must not cross
    labels = [('Без генератора', points_base, ORANGE, [False], [points_gen])]
    if points_gen:
        labels.append(
            ('З генератором', points_gen, GREEN, [True, False], [points_base])
        )
    for text, points, color, sides, others in labels:
        others = [line for line in others if line]
        box = d.textbbox((0, 0), text, font=f_line_label)
        big = Image.new(
            'RGBA',
            (math.ceil(box[2]) + 2 * LINE_SCALE, math.ceil(box[3]) + 2 * LINE_SCALE),
            (0, 0, 0, 0),
        )
        ImageDraw.Draw(big).text((LINE_SCALE, 0), text, fill=color, font=f_line_label)
        width = big.width / LINE_SCALE
        height = (box[3] - box[1]) / LINE_SCALE
        # the line with the generator lies under the orange line until its start: the label sits after that
        first_x = x_of(points[0][0])
        if points is points_gen and data['latest_start'] is not None:
            first_x = max(first_x, x_of(data['latest_start']))
        last_x = x_of(points[-1][0])
        # first the start of the night, above the line (the owner's choice: there it crosses no dashed line),
        # then the places where the line is straight under the label, then any place
        candidates = []
        for start, _ in spans:
            if now < start < end:
                candidates.append((True, True, x_of(start) + 8 + width / 2 + 4))
        for straight in [True, False]:
            for above in sides:
                for share in LINE_LABEL_SHARES:
                    candidates.append(
                        (straight, above, x_of(now + (end - now) * share))
                    )
        chosen = None
        for straight, above, cx in candidates:
            xa, xb = cx - width / 2 - 4, cx + width / 2 + 4
            if xa < max(LEFT, first_x) or xb > last_x:
                continue
            ya = y_of(_interpolate(points, moment_of(xa)))
            yb = y_of(_interpolate(points, moment_of(xb)))
            ym = y_of(_interpolate(points, moment_of(cx)))
            if straight and abs(ym - (ya + yb) / 2) > 2:
                continue
            length = math.hypot(xb - xa, yb - ya)
            ux, uy = (xb - xa) / length, (yb - ya) / length
            sign = 1 if above else -1
            offset = LINE_LABEL_GAP_PX + LINE_WIDTH / 2 + height / 2 + 2
            tx, ty = cx + sign * uy * offset, ym - sign * ux * offset
            clear = not _hits_line(
                (tx, ty),
                (ux, uy),
                (width, height),
                others,
                moment_of,
                y_of,
                _interpolate,
            )
            angle = math.degrees(math.atan2(ya - yb, xb - xa))
            turned = big.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
            turned = turned.resize(
                (
                    max(1, round(turned.width / LINE_SCALE)),
                    max(1, round(turned.height / LINE_SCALE)),
                ),
                Image.Resampling.LANCZOS,
            )
            left = round(tx - turned.width / 2)
            top = round(ty - turned.height / 2)
            place = (left, top, left + turned.width, top + turned.height)
            # inside the plot and above the red line of the zero point
            inside = TOP <= place[1] and place[3] <= y_of(zero) - 2
            if chosen is None:
                chosen = (turned, place)
            if inside and clear and not _overlaps(place, taken):
                chosen = (turned, place)
                break
        if chosen is not None:
            image.paste(chosen[0], (chosen[1][0], chosen[1][1]), chosen[0])
            taken.append(chosen[1])

    # under the chart: one line for each dot, with its sign before the words, and the time of the forecast
    y = HEIGHT - 104
    box = d.textbbox((0, 0), 'Пр', font=f_small)
    for kind, line in data['notes']:
        x = LEFT
        cy = y + (box[1] + box[3]) / 2
        if kind in ('empty', 'empty_gen'):
            color = ORANGE if kind == 'empty' else GREEN
            d.ellipse([x, cy - 6, x + 12, cy + 6], fill=color)
            x += 20
        d.text((x, y), line, fill=MUTED, font=f_small)
        y += 24
    label = f'Прогноз на {_hhmm(now)}'
    width = d.textlength(label, font=f_small)
    d.text((WIDTH - RIGHT - width, HEIGHT - 28), label, fill=MUTED, font=f_small)

    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    image.save(path)
    return path
