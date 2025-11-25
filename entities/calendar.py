# https://github.com/custom-components/pyscript
from imports_base import *
from entities.entity import Entity
from homeassistant.components.calendar import CalendarEvent

class Calendar(Entity):
    # noinspection PyMissingConstructor
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.init()

    def get_events(
        self,
        range_start: datetime | None = None,
        range_end: datetime | None = None,
    ) -> list[CalendarEvent]:
        range_start = range_start or dt_util.as_local(datetime.now())
        range_end = range_end or dt_util.as_local(datetime.now() + timedelta(days=1))

        events = calendar.get_events(
            entity_id=self.entity_id,
            start_date_time=range_start,
            end_date_time=range_end,
        )
        """
        {
            'calendar.kiiv_dtek_3_1_planned_outages': {
                'events': [
                    {
                        'description': 'Definite',
                        'end': '2025-11-04T22:00:00+02:00',
                        'start': '2025-11-04T19:30:00+02:00',
                        'summary': 'Planned Outage'
                    }
                ]
            }
        }
        """
        output = []
        if events:
            output = events.get(self.entity_id, {}).get('events', [])
            output = [
                CalendarEvent(
                    start=dt_util.as_local(dt_util.parse_datetime(_['start'])),
                    end=dt_util.as_local(dt_util.parse_datetime(_['end'])),
                    summary=_['summary'],
                    description=_['description'],
                ) for _ in output
            ]
        return output
